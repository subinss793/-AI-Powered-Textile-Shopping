from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/', views.register_user, name='register'),

    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('home', views.home, name='home'),
    path('category/<int:category_id>/', views.dresses_by_category, name='dresses_by_category'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('confirm-purchase/', views.confirm_purchase, name='confirm_purchase'),

 



]
