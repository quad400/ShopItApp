import json
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views import View

from .models import Cart, BillingAddress, Order
from .forms import CheckoutForm


def shop_cart(request):
    try:
        shopcart = Cart.objects.filter(ordered=False)
        total =0
        for cart in shopcart:
            total += cart.amount_price()
        context={
            'shopcart': shopcart,
            'total': total,
            }
        return render(request, 'order/shopcart.html', context=context)
    except ObjectDoesNotExist:
        messages.warning(request, "Your do not have active order")
        return render(request, 'order/shopcart.html')


@login_required(login_url='accounts/login') # Check login
def cart(request):
    shopcart = Cart.objects.filter(user_id=request.user.id, ordered=False)    
    order = Order.objects.get(user_id=request.user_id, ordered=False)
    context={
        'order': order,
        'shopcart': shopcart,       
        }
    return render(request, 'order/cart.html', context=context)



class CheckoutView(View):

    def get(self, *args, **kwargs):
        # form
        form = CheckoutForm()
        context = {
            'form': form,
        }


        return render(self.request, 'order/checkout.html', context)
        # return

    def post(self, *args, **kwargs):
        try:
            form = CheckoutForm(self.request.POST or None)
        
            if form.is_valid():
                order = Order.objects.get(user=self.request.user, ordered=False)
                street_address = form.cleaned_data["street_address"]
                print(street_address)
                apartment_address = form.cleaned_data["apartment_address"]
                country = form.cleaned_data["country"]
                zip = form.cleaned_data["zip"]
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                )

                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return HttpResponseRedirect('/')    
            else:
                messages.info(self.request, 'Please fill in required information')
                return HttpResponseRedirect('/shopcart')    

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return HttpResponseRedirect('/shopcart')

