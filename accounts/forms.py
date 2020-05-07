from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = "__all__"
		exclude = ["user"]

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
	address = forms.CharField(widget=forms.TextInput(attrs={
		"class": "form-control",
		"placeholder": "Address"
	}))
	city = forms.CharField(widget=forms.TextInput(attrs={
		"class": "form-control",
		"placeholder": "City"
	}))
	state = forms.CharField(widget=forms.TextInput(attrs={
		"class": "form-control",
		"placeholder": "State"
	}))
	zipcode = forms.CharField(widget=forms.TextInput(attrs={
		"class": "form-control",
		"placeholder": "Zipcode"
	}))
	payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)




