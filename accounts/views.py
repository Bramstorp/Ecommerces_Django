from django.http import HttpResponse
from django.http import JsonResponse

from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render, redirect 

import json
import datetime

from django.forms import inlineformset_factory

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.views.generic import View

# Create your views here.
from .models import *
from .forms import CreateUserForm, CustomerForm, CheckoutForm
from .decorator import unauthenticated_user, allowed_users, admin_only

def homepage(request):
	product = Product.objects.all()
	category = Category.objects.all()

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {"get_cart_total":0, "get_cart_items": 0}
		cartItems = order["get_cart_items"]
	
	context = {"product":product, "category":category, "cartItems":cartItems}
	return render(request, "accounts/home.html", context)

def contactpage(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {"get_cart_total":0, "get_cart_items": 0}
		cartItems = order["get_cart_items"]

	if request.method == 'POST':
		fullname = request.POST['fullname']
		phone = request.POST['phone']
		email = request.POST['email']
		message = request.POST['message']
		send_mail('Contact Form', message, fullname, phone, email, settings.EMAIL_HOST_USER,['EMAIL'], fail_silently=False)

	context = {"order":order, "cartItems":cartItems}
	return render(request, "accounts/contactpage.html", context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=["customer", "admin"])
def userpage(request, pk):
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	items = order.orderitem_set.all()
	cartItems = order.get_cart_items
	user = User.objects.get(id=pk)

	form = CustomerForm(instance=customer)

	context = {"order": order, "customer": customer, "items": items, "cartItems":cartItems, "user":user, "form":form}
	return render(request, "accounts/userpage.html", context)

@unauthenticated_user
def register(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'Account was created for ' + username)

			return redirect('loginpage')

	context = {'form':form}
	return render(request, "accounts/register.html", context)

@unauthenticated_user
def loginpage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('homepage')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/loginpage.html', context)

def logoutUser(request):
	logout(request)
	return redirect('homepage')

def product(request, pk):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {"get_cart_total":0, "get_cart_items": 0}
		cartItems = order["get_cart_items"]
	
	product = Product.objects.get(id=pk)
	
	context = {"product": product, "order": order, "items": items, "cartItems": cartItems}
	return render(request, "accounts/viewproduct.html", context)

@login_required(login_url='loginpage')
def checkout(request):
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	items = order.orderitem_set.all()
	cartItems = order.get_cart_items

	context = {"order": order, "customer": customer, "items": items, "cartItems": cartItems}
	return render(request, "accounts/checkout.html", context)

@login_required(login_url='loginpage')
def cart(request):
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	items = order.orderitem_set.all()
	cartItems = order.get_cart_items

	context = {"order": order, "customer": customer, "items": items, "cartItems":cartItems}
	return render(request, "accounts/cart.html", context)

@login_required(login_url='login')
def updateItem(request):
	data = json.loads(request.body)
	productId = data["productId"]
	action = data["action"]
	#print("action", action)
	#print("productId", productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == "add":
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == "remove":
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse("item was added", safe=False)

@login_required(login_url='loginpage')
def order_complete(request):
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	items = order.orderitem_set.all()
	cartItems = order.get_cart_items

	context = {"order": order, "customer": customer, "items": items, "cartItems":cartItems}
	return render(request, "accounts/order_complete.html", context)

@login_required(login_url='loginpage')
def checkout(request):
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	items = order.orderitem_set.all()
	cartItems = order.get_cart_items
	
	form = CheckoutForm(request.POST)
	if request.method == "POST":
		if form.is_valid():
			transaction_id = datetime.datetime.now().timestamp()
			address = form.cleaned_data.get("address")
			city = form.cleaned_data.get("city")
			state = form.cleaned_data.get("state")
			zipcode = form.cleaned_data.get("zipcode")
			payment_option = form.cleaned_data.get("payment_option")
			
			order.transaction_id = transaction_id
			order.complete = True
			
			shipping_address = ShippingOrder(
				customer = request.user.customer,
				order = order,
				address = address,
				city = city,
				state = state,
				zipcode = zipcode,
				payment = payment_option
			)
				
			order.save()
			shipping_address.save()

			return redirect("order_complete")
		messages.warning(request, "Failed checkout")
		return redirect("cart")

	context = {"form":form, "order": order, "customer": customer, "items": items, "cartItems":cartItems}
	return render(request, "accounts/checkout.html", context)