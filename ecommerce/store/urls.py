from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from . import views

urlpatterns = [
    path('user/', views.user_profile, name='user_profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_change/', PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('orders/', views.orders_view, name='orders'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('address/add/', views.add_address, name='add_address'),
    path('address/edit/<int:address_id>/', views.edit_address, name='edit_address'),
    path('address/delete/<int:address_id>/', views.delete_address, name='delete_address'),
    path('address/list/', views.address_list, name='address_list'),
    path('card/add/', views.add_card, name='add_card'),
    path('card/edit/<int:card_id>/', views.edit_card, name='edit_card'),
    path('card/delete/<int:card_id>/', views.delete_card, name='delete_card'),
    path('card/list/', views.card_list, name='card_list'),
    path('address/list/', views.address_list, name='address_list'),

]
