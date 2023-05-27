from django.contrib import admin

from .models import Cart, Order, BillingAddress

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['product','user','quantity','get_price']
    list_display_link = ['product']
    list_filter = ['ordered']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',]
    list_filter = ['ordered']



admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress)
