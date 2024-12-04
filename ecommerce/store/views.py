from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required(login_url='/login/')  # Login gerektirir, login yapılmadıysa login sayfasına yönlendirir
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

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
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', 'product_list')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')