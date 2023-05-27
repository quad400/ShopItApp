from django import forms
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

from .models import Cart


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

class CheckoutForm(forms.Form):

    # PAYMENT_CHOICES = (
    #     ('S', 'Stripe'),
    #     ('P', 'Paypal'),
    # )

    street_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder':'Street Address'}))
    apartment_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder':'Apartment Address'}),required=False)
    country = CountryField(blank_label='(select country)', ).formfield(
                        widget=CountrySelectWidget(attrs={'class': 'input form-control'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder':'Zip'}))
    # same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    # save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    # payment_option = forms.ChoiceField(widget=forms.RadioSelect(),
    #         choices=PAYMENT_CHOICES
    # )
