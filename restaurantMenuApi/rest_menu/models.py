from django.db import models
from django.contrib.auth.models import User

class Category (models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class MenuItem (models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    ingridiants = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images', null=True)
    category = models.ForeignKey(
        Category, related_name="category", on_delete=models.PROTECT, default=None
    )
    

    def __str__(self) -> str:
        return self.name

class Order (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deliverd_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.BooleanField(default=False)
    items = models.ManyToManyField(MenuItem,  through='OrderItem')

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem (models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"   