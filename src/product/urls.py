from django.urls import path

from .views import (home_page, ajax_variant, category_product, 
                    product_detail, addcomment, add_to_cart, remove_product_from_cart, 
                    remove_single_quantity_product, search, faq)

urlpatterns = [
     path('', home_page, name='home_page'),
    path('ajax_variant', ajax_variant, name='ajax_variant'),
    # product
    path('search', search, name='search'),
    path('faq', faq, name='faq'),
    path('category/<int:id>/<slug:slug>', 
                    category_product, name='category_product'),
    path('product/<int:id>/<slug:slug>', 
                    product_detail, name='product_detail'),
    path('product/addcomment/<int:id>', addcomment, name='addcomment'),
    path('addtocart/<int:id>', add_to_cart, name='addtocart'),
    path('remove-product-from-cart/<int:id>', remove_product_from_cart, name='remove-product-from-cart'),
    path('remove-single-quantity-product/<int:id>', 
                remove_single_quantity_product, 
                name='remove-single-quantity-product'), 
]