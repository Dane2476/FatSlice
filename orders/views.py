from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
# Our views name is login, so we're changing the login function name to auth_login
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import RegistrationForm, LoginForm, PizzaForm
from .models import PizzaSize, SicilianSize, Sub, Salad, Pasta, DinnerPlatter, Topping, SubExtra, CreatedItem, UserOrder

from decimal import *

def index(request):
    subs = Sub.objects.all()
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    dinnerPlatters = DinnerPlatter.objects.all()
    toppings = Topping.objects.all()

    context = {
    "toppings": toppings,
    "subs": subs,
    "pastas":pastas,
    "salads":salads,
    "dinnerPlatters": dinnerPlatters,
    }
    return render(request, "orders/index.html", context)

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/order')

    if request.method == "GET":
        form = RegistrationForm()
        return render(request, "orders/register.html", {"form" : form})

    if request.method =="POST":
        form = RegistrationForm(request.POST)

        # Check if the form's passwords match and all inputs are filled
        if form.is_valid():
            # Removes all markup from our form
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            # Create a user, password is automatically hashed
            User.objects.create_user(username=username, email=None, password=password)

            # The authenticate function checks if the credentials are valid,
            # returning the user object (username) if they are, None if not.
            user = authenticate(username=username, password=password)

            # Log user in and redirect to the order page
            auth_login(request, user)
            return HttpResponseRedirect('/order')
        else:
            return render(request, "orders/register.html", {"form" : form})


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/order')
    if request.method == "GET":
        form = LoginForm()
        return render(request, "orders/login.html", {"form": form})
    if request.method == "POST":

        # Similar logic to our registration view, check form inputs and then authenticate
        form = LoginForm(request=request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # if the credentials are valid, login user and redirect to order page
            user = authenticate(username = username, password=password)
            auth_login(request, user)
            return HttpResponseRedirect('/order')
        else:
            return render(request, "orders/register.html", {"form" : form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

# redirect to register page if user has not logged in
@login_required(login_url='/register')
def order(request):
    
    pizza = PizzaForm()
    subs = Sub.objects.all()
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    dinnerPlatters = DinnerPlatter.objects.all()
    extras = SubExtra.objects.all()
    context = {
        "pizza" : pizza,
        "subs" : subs,
        "pastas" : pastas,
        "salads" : salads,
        "dinnerPlatters" : dinnerPlatters,
        "extras" : extras,
    }

    user = request.user

    if request.method == "GET":

        return render(request, "orders/order.html", context)
    if request.method == "POST":
        if 'pizza-order' in request.POST:
            print(request.POST.get)
            size = request.POST.get('size')
            toppingsAllowed = request.POST.get('toppingsAllowed')

            # Filter through our PizzaSize model, get the price of the selected size
            price = PizzaSize.objects.get(size=size).price
            # Get the price of one topping based on our pizza's size
            toppingPrice = PizzaSize.objects.get(size=size).toppingPrice

            toppingPrice = toppingPrice * Decimal(toppingsAllowed)
            price += toppingPrice

            # Gets a list of all selected toppings
            toppings = request.POST.getlist('toppings')

            if len(toppings) > int(toppingsAllowed):
                raise forms.ValidationError("Too many toppings")

            toppings = ' '.join(toppings) # Creating a string out of our list of toppings
            item = size + " " + toppingsAllowed + " topping Regular Pizza - " + toppings

            item = CreatedItem(user=user, item=item, price=price)
            item.save()
            messages.success(request, 'Regular Pizza added to cart!')
        elif 'sicilian-order' in request.POST:
            size = request.POST.get('size')
            toppingsAllowed = request.POST.get('toppingsAllowed')

            # Filter through our PizzaSize model, get the price of the selected size
            price = SicilianSize.objects.get(size=size).price
            # Get the price of one topping based on our pizza's size
            toppingPrice = SicilianSize.objects.get(size=size).toppingPrice

            toppingPrice = toppingPrice * Decimal(toppingsAllowed)
            price += toppingPrice

            # Gets a list of all selected toppings
            toppings = request.POST.getlist('toppings')

            if len(toppings) > int(toppingsAllowed):
                raise forms.ValidationError("Too many toppings")

            toppings = ' '.join(toppings) # Creating a string out of our list of toppings
            item = size + " " + toppingsAllowed + " topping Sicilian Pizza - " + toppings

            item = CreatedItem(user=user, item=item, price=price)
            item.save()
            messages.success(request, 'Sicilian Pizza added to cart!')
        elif 'sub-order' in request.POST:
            sub = request.POST.get('sub')
            extras = request.POST.getlist('extras')
            sub = sub.split('|')
            name = sub[0]
            price = float(sub[1])
            if price > 7.50:
                size = "Large"
            else:
                size = "Small"
            for extra in extras:
                price += .50
            extras = ' '.join(extras)
            item = size + " " + name + " Sub - " + extras
            item = CreatedItem(user=user, item=item, price=price)
            item.save()
            messages.success(request, 'Sub added to cart!')
        elif 'pasta-order' in request.POST:
            pasta = request.POST.get('pasta')
            pasta = pasta.split('|')
            name = pasta[0]
            price = float(pasta[1])

            item = CreatedItem(user=user, item=name, price=price)
            item.save()
            messages.success(request, 'Pasta added to cart!')
        elif 'salad-order' in request.POST:
            salad = request.POST.get('salad')
            salad = salad.split('|')
            name = salad[0]
            price = float(salad[1])

            item = CreatedItem(user=user, item=name, price=price)
            item.save()
            messages.success(request, 'Salad added to cart!')
        elif 'platter-order' in request.POST:
            platter = request.POST.get('platter')
            platter = platter.split('|')
            name = platter[0]
            price = float(platter[1])
            if price > 45.00:
                size = "Large"
            else:
                size = "Small"
            item = size + " " + name + " Platter"
            item = CreatedItem(user=user, item=item, price=price)
            item.save()
            messages.success(request, 'Dinner Platter added to cart')
        return render(request, "orders/order.html", context)

@login_required(login_url='/register')
def cart(request):
    user = request.user
    items = CreatedItem.objects.filter(user=user) # Get items in users cart
    total = 0
    for item in items:
        total += item.price
    if request.method == "GET":
        return render(request, "orders/cart.html", {"items": items, "total" : total})

    if request.method == "POST":
        # This is for the deletion of an object from the cart
        if 'pk' in request.POST:
            # Get the primary key of the item being deleted by user
            pk = request.POST.get('pk')
            # Make sure that the user didnt manipulate the primary key
            CreatedItem.objects.filter(user=user, pk=pk).delete() # if they didnt, delete the item
            # Re-query DB for updated cart items
            items = CreatedItem.objects.filter(user=user)
            total = 0
            for item in items:
                total += item.price
            return render(request, "orders/cart.html", {"items": items, "total": total})

        elif 'order' in request.POST:
            # I'm creating a text field here for the UserOrder model
            userItems = ""
            for item in items:
                userItems += item.item + "\n"
            order = UserOrder(user=user, items=userItems, total=total)
            order.save()

            cart = CreatedItem.objects.filter(user=user).delete()
            return HttpResponseRedirect('/orders')

        return render(request, "orders/cart.html", {"items": items, "total": total})

@login_required(login_url='/register')
def orders(request):
    user = request.user
    orders = UserOrder.objects.filter(user=user)
    for order in orders:
        print(order.items)
    if request.method == "GET":
        return render(request, 'orders/orders.html', {"orders": orders})
