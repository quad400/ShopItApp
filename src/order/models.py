from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from django_countries.fields import CountryField

from product.models import Product
User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.product.title

    def get_price(self):
        return self.product.price

    def get_discount_price(self):
        return self.product.discount_price

    def amount_price(self):
        if self.get_discount_price():
            return self.get_discount_price() * self.quantity
        return self.get_price() * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL,
                blank=True, null=True
    )


    def __str__(self):
        return self.user.username
        
    def get_total(self):
        total = 0
        for calc in self.cart.all():
            total+=calc.amount_price()
        print('total: ', total)
        return total



class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=300)
    apartment_address = models.CharField(max_length=300)
    country = CountryField(multiple=True)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
