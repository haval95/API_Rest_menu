from .models import  MenuItem
from django_filters import rest_framework as filters

class MenuItemsFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    class Meta: 
        model=MenuItem
        fields=["price", "category"]