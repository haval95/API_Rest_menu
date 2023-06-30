from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from .models import MenuItem, Category, Cart, CartItem
from .serializers import (
    MenuItemSerializer,
    CategorySerializer,
    UserSerializer,
    CartItemSerializer,
    CartSerializer
)
from .permissions import ManagerOnlyPermission, CustomerOnlyPermission
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


class CartItemView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [CustomerOnlyPermission]
    
    
class DeleteSingleCartItemView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [CustomerOnlyPermission]
    
class DeleteCartView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [CustomerOnlyPermission]

    def get_object(self):
        # Get the current user's cart
        user = self.request.user
        cart = Cart.objects.get(user=user)
        return cart
    


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
        return Response({"message": "User Not Found"}, status.HTTP_400_BAD_REQUEST)


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


class DeliveryUsersList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [ManagerOnlyPermission]

    def get_queryset(self):
        return User.objects.filter(groups__name="delivery").all()

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        if username:
            user = get_object_or_404(User, username=username)
            delivery = Group.objects.get(name="delivery")
            delivery.user_set.add(user)
            return Response(status=status.HTTP_201_CREATED)
        return Response({"message": "User Not Found"}, status.HTTP_400_BAD_REQUEST)


class RemoveUserFromDeliveryGroup(generics.DestroyAPIView):
    permission_classes = [ManagerOnlyPermission]

    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        delivery = Group.objects.get(name="delivery")
        delivery.user_set.remove(user)
        return Response(status=status.HTTP_200_OK)
