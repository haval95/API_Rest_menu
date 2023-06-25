from django.shortcuts import render
from rest_framework import  generics, permissions
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from .permissions import ManagerOnlyPermission



    
    
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related("category").all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [permissions.IsAuthenticated, ManagerOnlyPermission]
        return [permission() for permission in permission_classes]
            

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.select_related("category").all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [permissions.IsAuthenticated, ManagerOnlyPermission]
        return [permission() for permission in permission_classes]
    
    
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [permissions.IsAuthenticated, ManagerOnlyPermission]
        return [permission() for permission in permission_classes]


class SingleCategoryView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [permissions.IsAuthenticated, ManagerOnlyPermission]
        return [permission() for permission in permission_classes]

