from django.urls import path

from .views import shop_cart,cart, CheckoutView

urlpatterns = [
 
    path('shopcart', shop_cart, name='shop-cart'),
    path('cart', cart, name='cart'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
]