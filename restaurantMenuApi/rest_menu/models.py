from django.db import models


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

