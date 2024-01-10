from django.urls import path
from .views import (
    MenuItemView,
    SingleMenuItemView,
    CategoryView,
    SingleCategoryView,
    CartItemView,
    ManagerUsersList,
    RemoveUserFromManagerGroup,
    DeliveryUsersList,
    RemoveUserFromDeliveryGroup,
    DeleteSingleCartItemView,
    DeleteCartView,
    OrderView,
    SingleOrderView,
)

urlpatterns = [
    path("menu-items/", MenuItemView.as_view()),
    path("menu-items/<int:pk>", SingleMenuItemView.as_view()),
    path("categories/", CategoryView.as_view()),
    path("categories/<int:pk>", SingleCategoryView.as_view()),
    path("cart/menu-items", CartItemView.as_view()),
    path("cart/menu-items/<int:pk>", DeleteSingleCartItemView.as_view()),
    path("cart", DeleteCartView.as_view()),
    path("orders", OrderView.as_view()),
    path("orders/<int:pk>", SingleOrderView.as_view()),
    path("groups/manager/users", ManagerUsersList.as_view()),
    path("groups/manager/users/<int:user_id>", RemoveUserFromManagerGroup.as_view()),
    path("groups/delivery-crew/users", DeliveryUsersList.as_view()),
    path(
        "groups/delivery-crew/users/<int:user_id>",
        RemoveUserFromDeliveryGroup.as_view(),
    ),
]
