from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, Order, Cart
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required(login_url='/login/')  # Login gerektirir, login yapılmadıysa login sayfasına yönlendirir
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
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews, 'all_products': all_products})

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
    return render(request, 'login.html', {'next': request.GET.get('next', '')})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).select_related('product')

    return render(request, 'user.html', {'user': user, 'orders': orders})

@login_required
def orders_view(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'orders.html', {'orders': orders})