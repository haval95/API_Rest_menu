from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from .models import MenuItem, Category, Cart, CartItem, Order, OrderItem
from .serializers import (
    MenuItemSerializer,
    CategorySerializer,
    UserSerializer,
    CartItemSerializer,
    CartSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from .permissions import ManagerOnlyPermission, CustomerOnlyPermission
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related("category").all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [permissions.IsAuthenticated, ManagerOnlyPermission]
        return [permission() for permission in permission_classes]


class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.select_related("category").all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [permissions.IsAuthenticated, ManagerOnlyPermission]
        return [permission() for permission in permission_classes]


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [permissions.IsAuthenticated, ManagerOnlyPermission]
        return [permission() for permission in permission_classes]


class SingleCategoryView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [permissions.IsAuthenticated, ManagerOnlyPermission]
        return [permission() for permission in permission_classes]


class CartItemView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [CustomerOnlyPermission]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class DeleteSingleCartItemView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [CustomerOnlyPermission]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class DeleteCartView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [CustomerOnlyPermission]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_object(self):
        # Get the current user's cart
        user = self.request.user
        cart = Cart.objects.get(user=user)
        return cart


class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_throttles(self):
        if self.request.method == "POST":
            throttle_classes = [AnonRateThrottle, UserRateThrottle]
        else:
            throttle_classes = []  # No throttling for other methods
        return [throttle() for throttle in throttle_classes] 

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="customer").exists():
            queryset = Order.objects.filter(user=user)
        elif user.groups.filter(name="manager").exists():
            queryset = Order.objects.all()
        elif user.groups.filter(name="delivery").exists():
            queryset = Order.objects.filter(delivery_crew=user)  

        pending = self.request.query_params.get("pending")
        if pending:
            queryset = queryset.filter(status=pending)
        return queryset
        
    def create(self, request, *args, **kwargs):
        # Get the current user
        user = self.request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"message": "Cart is empty"}, status=status.HTTP_404_NOT_FOUND)
       

        # Create the order
        order = Order.objects.create(user=user)

        # Get the cart items and create order items based on them
        cart_items = cart.items.all()
        order_items = []
        total = 0
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=cart_item.total_price,
            )
            total += cart_item.total_price

            order_items.append(order_item)

        order.total = total
        order.save()
        # Delete the cart
        cart.delete()

        # Serialize the order and order items
        serializer = self.get_serializer(order)
        data = serializer.data
        data["order_items"] = OrderItemSerializer(order_items, many=True).data

        return Response(data)


class SingleOrderView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="customer").exists():
            queryset = Order.objects.filter(user=user)
        elif user.groups.filter(name="manager").exists():
            queryset = Order.objects.all()
        elif user.groups.filter(name="delivery").exists():
            queryset = Order.objects.filter(delivery_crew=user)
        return queryset
    
    def put(self, request, *args, **kwargs):
        # Allow PUT method for managers
        user = self.request.user
        if user.groups.filter(name="manager").exists():
            return self.update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        # Allow PATCH method for managers
        user = self.request.user
        if user.groups.filter(name="manager").exists():
            return self.partial_update(request, *args, **kwargs)
        elif user.groups.filter(name="delivery").exists():
            order = self.get_object()  # Get the order object
            order.status = not order.status  # Reverse the status value
            if order.status:  # If the status is True, update delivered_at
                order.delivered_at = timezone.now()
            else:  # If the status is False, set delivered_at to None
                order.delivered_at = None
            order.save()  # Save the updated order

            serializer = self.get_serializer(order)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if user.groups.filter(name="manager").exists():
            return self.destroy(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
   
    


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
