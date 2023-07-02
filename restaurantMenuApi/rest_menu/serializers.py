from rest_framework import serializers
from .models import MenuItem, Category, Cart, CartItem, Order, OrderItem
from django.contrib.auth.models import User, Group


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField()

    class Meta:
        model = MenuItem
        fields = ["name", "price", "featured", "ingridiants", "image", "category", "category_id"]


class SimpleMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "groups"]


class CartItemSerializer(serializers.ModelSerializer):
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source="menu_item", write_only=True
    )
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "menu_item",
            "quantity",
            "unit_price",
            "menu_item_id",
            "total_price",
        ]

    def create(self, validated_data):
        # Get the menu_item and quantity from the validated data
        menu_item = validated_data["menu_item"]
        quantity = 1
        if "quantity" in self.context["request"].data:
            quantity = validated_data["quantity"]
        # Get the current user
        user = self.context["request"].user

        # Try to retrieve the user's existing cart
        cart = Cart.objects.filter(user=user).first()

        if cart:
            # Check if a CartItem with the same menu_item exists in the cart
            cart_item = CartItem.objects.filter(cart=cart, menu_item=menu_item).first()

            if cart_item:
                # If the CartItem exists, update the quantity
                cart_item.quantity += quantity
                cart_item.total_price = cart_item.quantity * cart_item.unit_price
                cart_item.save()
            else:
                # If the CartItem does not exist, create a new one
                cart_item = CartItem.objects.create(
                    cart=cart,
                    menu_item=menu_item,
                    quantity=quantity,
                    unit_price=menu_item.price,
                    total_price=menu_item.price * quantity,
                )

        else:
            # If the cart doesn't exist, create a new cart and add the item to it
            cart = Cart.objects.create(user=user)
            cart_item = CartItem.objects.create(
                cart=cart,
                menu_item=menu_item,
                quantity=quantity,
                unit_price=menu_item.price,
                total_price=menu_item.price * quantity,
            )

        return cart_item


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
