from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    ingridiants = models.CharField(max_length=500)
    image = models.ImageField(upload_to="images", null=True)
    featured = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, related_name="category", on_delete=models.PROTECT, default=None
    )

    def __str__(self) -> str:
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart (User: {self.user.username})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveIntegerField(null=True)
    total_price = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"CartItem ({self.menu_item.name})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveIntegerField(null=True)
    total_price = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"
