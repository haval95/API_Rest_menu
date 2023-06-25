from django.shortcuts import get_object_or_404
from rest_framework import  generics, permissions, status
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer
from .permissions import ManagerOnlyPermission
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
    
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



class ManagerUsersList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [ManagerOnlyPermission]
    
    def get_queryset(self):
        return User.objects.filter(groups__name="manager").all()
    
    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="manager")
            managers.user_set.add(user)
            return Response(status=status.HTTP_201_CREATED)
        return Response({"msg": "error"}, status.HTTP_400_BAD_REQUEST)
    
class RemoveUserFromManagerGroup(generics.DestroyAPIView):
    permission_classes = [ManagerOnlyPermission]
    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        managers = Group.objects.get(name="manager")
        managers.user_set.remove(user)
        return Response(status=status.HTTP_200_OK)
    