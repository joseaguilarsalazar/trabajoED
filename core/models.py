from django.contrib.auth.models import User
from django.db import models

# 1. User model (using Django's built-in User)

# 2. Dish model - represents a dish available for purchase
class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

# 3. Shopping Cart - temporary items before purchase
class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish, related_name="cart_items", blank=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        return sum(dish.price for dish in self.dishes.all())

# 4. Order - completed purchase
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish, related_name="orders")
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - ${self.total}"

# 5. Payment - simulation of a payment
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {'Success' if self.success else 'Failed'}"
