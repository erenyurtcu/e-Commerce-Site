from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, Order, Cart, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Arama ve kategori filtreleme işlemi yapan ortak fonksiyon
def get_filtered_products(request):
    query = request.GET.get('search', '')
    category_id = request.GET.get('category', None)
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    if category_id:
        products = products.filter(category__id=category_id)

    return products, query, category_id


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def cart_view(request):
    categories = Category.objects.all()
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'categories': categories})

def product_list(request):
    products, query, category_id = get_filtered_products(request)
    categories = Category.objects.all()
    return render(request, 'product_list.html', {'products': products, 'categories': categories, 'query': query, 'category_id': category_id})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    all_products = Product.objects.exclude(id=id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Yorum ekle
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
        return redirect('product_detail', id=id)

    reviews = product.reviews.all()
    categories = Category.objects.all()
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews, 'all_products': all_products, 'categories': categories})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or 'product_list'
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    categories = Category.objects.all()
    return render(request, 'login.html', {'next': request.GET.get('next', ''), 'categories': categories})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).select_related('product')
    categories = Category.objects.all()
    return render(request, 'user.html', {'user': user, 'orders': orders, 'categories': categories})

@login_required
def orders_view(request):
    user = request.user
    orders = Order.objects.filter(user=request.user).select_related('product')
    categories = Category.objects.all()
    return render(request, 'orders.html', {'orders': orders, 'categories': categories})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')
    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity
        )
    cart_items.delete()
    return render(request, 'checkout.html', {'message': 'Your order has been placed successfully!'})
