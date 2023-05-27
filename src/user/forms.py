from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from .models import UserProfile

class UserUpdate(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'input', 'placeholder':'Username'}),
            'email' : forms.EmailInput(attrs={'class': 'input', 'placeholder':'Email'}),
            'first_name' : forms.TextInput(attrs={'class': 'input', 'placeholder':'First Name'}),
            'last_name' : forms.TextInput(attrs={'class': 'input', 'placeholder':'Last Name'})
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'zip', 'city', 'country', 'image']
        widgets = {
            'phone' : forms.TextInput(attrs={'class': 'input', 'placeholder':'phone'}),
            'address' : forms.TextInput(attrs={'class': 'input', 'placeholder':'address'}),
            'zip' : forms.TextInput(attrs={'class': 'input', 'placeholder':'zip'}),
            'city' : forms.TextInput(attrs={'class': 'input', 'placeholder':'city'}),
            'country' : forms.TextInput(attrs={'class': 'input', 'placeholder':'country'}),
            'image': forms.FileInput(attrs={'class': 'input', 'placeholder':'image'})
        }
