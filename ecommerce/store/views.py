from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, Order, Cart, Category, Card, Address
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest


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


@login_required
def add_address(request):
    """Yeni bir adres ekleme."""
    if request.method == 'POST':
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        is_default = request.POST.get('is_default') == 'on'

        if street and city and postal_code and country:
            # Eğer yeni adres default olarak işaretlenmişse, diğer adresleri default olmaktan çıkar
            if is_default:
                Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

            Address.objects.create(
                user=request.user,
                street=street,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
                is_default=is_default
            )
            return redirect('address_list')
        else:
            return HttpResponseBadRequest("All required fields must be provided.")

    return render(request, 'add_address.html')


@login_required
def edit_address(request, address_id):
    """Mevcut bir adresi düzenleme."""
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        address.street = request.POST.get('street', address.street)
        address.city = request.POST.get('city', address.city)
        address.state = request.POST.get('state', address.state)
        address.postal_code = request.POST.get('postal_code', address.postal_code)
        address.country = request.POST.get('country', address.country)
        is_default = request.POST.get('is_default') == 'on'

        # Eğer bu adres default olarak işaretlenmişse, diğer adresleri default olmaktan çıkar
        if is_default:
            Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

        address.is_default = is_default
        address.save()
        return redirect('address_list')

    return render(request, 'edit_address.html', {'address': address})


@login_required
def add_card(request):
    """Yeni bir kart ekleme."""
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        cardholder_name = request.POST.get('cardholder_name')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        is_default = request.POST.get('is_default') == 'on'

        if card_number and cardholder_name and expiry_date and cvv:
            Card.objects.create(
                user=request.user,
                card_number=card_number,
                cardholder_name=cardholder_name,
                expiry_date=expiry_date,
                cvv=cvv,
                is_default=is_default
            )
            return redirect('card_list')
        else:
            return HttpResponseBadRequest("All required fields must be provided.")

    return render(request, 'add_card.html')


@login_required
def edit_card(request, card_id):
    """Mevcut bir kartı düzenleme."""
    card = get_object_or_404(Card, id=card_id, user=request.user)

    if request.method == 'POST':
        card.card_number = request.POST.get('card_number', card.card_number)
        card.cardholder_name = request.POST.get('cardholder_name', card.cardholder_name)
        card.expiry_date = request.POST.get('expiry_date', card.expiry_date)
        card.cvv = request.POST.get('cvv', card.cvv)
        card.is_default = request.POST.get('is_default') == 'on'
        card.save()
        return redirect('card_list')

    return render(request, 'edit_card.html', {'card': card})


@login_required
def delete_address(request, address_id):
    """Mevcut bir adresi silme."""
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return redirect('address_list')

@login_required
def delete_card(request, card_id):
    """Mevcut bir kartı silme."""
    card = get_object_or_404(Card, id=card_id, user=request.user)
    card.delete()
    return redirect('card_list')

@login_required
def address_list(request):
    """Kullanıcının tüm adreslerini listeleme."""
    addresses = Address.objects.filter(user=request.user)
    categories = Category.objects.all()
    return render(request, 'address_list.html', {'addresses': addresses, 'categories': categories})

@login_required
def card_list(request):
    """Kullanıcının tüm kartlarını listeleme."""
    cards = Card.objects.filter(user=request.user)
    categories = Category.objects.all()
    return render(request, 'card_list.html', {'cards': cards, 'categories': categories})
