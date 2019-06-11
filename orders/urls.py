from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout_view"),
    path("login", views.login, name="login"),
    path("order", views.order, name="order"),
    path("cart", views.cart, name="cart"),
    path("orders", views.orders, name="orders"),

]
