from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"), 
    path("contact/", views.contactpage, name="contactpage"),
    path("dashboard/<str:pk>/", views.userpage, name="userpage"),
    path("product/<str:pk>/", views.product, name="product"),
	
	path("cart/", views.cart, name="cart"),
    path('checkout/', views.checkout, name='checkout'),
    path("order_complete/", views.order_complete, name="order_complete"),

    path("update_item/", views.updateItem, name="updateItem"),

    path("register/", views.register, name="register"),
    path("login/", views.loginpage, name="loginpage"),
    path("logoutUser/", views.logoutUser, name="logoutUser"),
]