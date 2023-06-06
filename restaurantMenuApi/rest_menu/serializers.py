from rest_framework import serializers
from .models import MenuItem, Category

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Category
        fields= "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField()
    class Meta:
        model= MenuItem
        fields= ["name", "price", "ingridiants", "image", "category", "category_id"]