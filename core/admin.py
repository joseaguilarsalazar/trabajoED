from django.contrib import admin
from .models import Dish, ShoppingCart, Order, Payment

admin.site.register(Dish)
admin.site.register(ShoppingCart)
admin.site.register(Order)
admin.site.register(Payment)
