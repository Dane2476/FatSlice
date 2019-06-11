from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import PizzaSize, SicilianSize, Sub, Salad, Pasta, DinnerPlatter, Topping, SubExtra, UserOrder


# We're altering Djangos built in UserCreationForm to give our form different attributes
# Using Django widgets
class RegistrationForm(UserCreationForm):

    password1 = forms.CharField(
        label =("Password"),
        # Look at Django widgets documentation for different input options
        widget = forms.PasswordInput(attrs={
            'placeholder' : ' Password'
        }),
        help_text = "<br>8 characters or more"
    )
    password2 = forms.CharField(
        label =("Password confirmation"),
        widget = forms.PasswordInput(attrs={
            'placeholder' : ' Confirm Password'
        })
    )

    # We're altering the placeholder for the username field here
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True,
                                                                          'placeholder':'Username'})
        self.fields[self._meta.model.USERNAME_FIELD].help_text = '<br>150 characters or fewer.<br>Letters, digits and @/./+/-/_ only.'

# Same thing here for the login form... we're just altering AuthenticationForm here to add
# Different attributes
class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label = ("Username"),
        widget = forms.TextInput(attrs={
            'placeholder' : ' Username'
        })
    )

    password = forms.CharField(
        label =("Password"),
        widget = forms.PasswordInput(attrs={
            'placeholder' : ' Password'
        })
    )


# Creating our pizza form to pass into Orders.html
class PizzaForm(forms.Form):
    def getPizzaChoices():
        choices = []
        for choice in choices:
            choices.append((pizza.price, pizza.size))
        return choices

    size = forms.ChoiceField(
        choices= getPizzaChoices,
        label="Size: "
    )
    toppingsAllowed = (
        ('0', 'Cheese'),
        ('1', '1 Topping'),
        ('2', '2 Topping'),
        ('3', '3 Topping'),
        ('5', 'Special')
    )
    toppingsAllowed = forms.ChoiceField(
        choices=toppingsAllowed,
        label='',
        widget=forms.RadioSelect(),
    )
    toppings = forms.ModelChoiceField(
        queryset=Topping.objects.values_list("topping", flat=True),
        label='Toppings',
        empty_label = None,
        widget=forms.CheckboxSelectMultiple
    )
