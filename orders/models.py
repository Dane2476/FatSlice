from django.conf import settings
from django.db import models
from django.contrib.auth.models import User



# Menu Models
class PizzaSize(models.Model):
    size = models.CharField(max_length=24) # Small / Large
    price = models.DecimalField(max_digits=5, decimal_places=2) # $14.99
    toppingPrice = models.DecimalField(max_digits=5, decimal_places=2) # $ 2.99

    def __str__(self):
        return f"{self.size}: {self.price} (toppings: ${self.toppingPrice} each)"

class SicilianSize(models.Model):
    size = models.CharField(max_length=24)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    toppingPrice = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.size}: {self.price} (toppings: ${self.toppingPrice} each)"

class Sub(models.Model):
    name = models.CharField(max_length=24)
    smallPrice = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    largePrice = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} - small: ${self.smallPrice} large: ${self.largePrice}"

class Salad(models.Model):
    name = models.CharField(max_length=24)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}: {self.price}"

class Pasta(models.Model):
    name = models.CharField(max_length=24)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}: {self.price}"

class DinnerPlatter(models.Model):
    name = models.CharField(max_length=24)
    smallPrice = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    largePrice = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} - small: ${self.smallPrice} large: ${self.largePrice}"

class Topping(models.Model):
    topping = models.CharField(max_length=24)

    def __str__(self):
        return f"{self.topping}"

class SubExtra(models.Model):
    extra = models.CharField(max_length=24)

    def __str__(self):
        return f"{self.extra}"

class CreatedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return f"{self.item} - {self.price}"


class UserOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.AutoField(primary_key=True)
    items = models.TextField()
    total = models.DecimalField(max_digits=5, decimal_places=2)
    is_ordered = models.BooleanField(default=True)
    is_fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} order #{self.order_number}"
