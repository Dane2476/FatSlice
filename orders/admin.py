from django.contrib import admin
from .models import PizzaSize, SicilianSize, Sub, Salad, Pasta, DinnerPlatter, Topping, SubExtra, CreatedItem, UserOrder
# Register your models here.
admin.site.register(PizzaSize)
admin.site.register(SicilianSize)
admin.site.register(Sub)
admin.site.register(Salad)
admin.site.register(Pasta)
admin.site.register(DinnerPlatter)
admin.site.register(Topping)
admin.site.register(SubExtra)
admin.site.register(UserOrder)
admin.site.register(CreatedItem)
