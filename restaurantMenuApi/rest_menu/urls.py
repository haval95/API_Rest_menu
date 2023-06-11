from django.urls import path
from .views import MenuItemView, SingleMenuItemView, CategoryView, SingleCategoryView

urlpatterns = [
    path("menu-items", MenuItemView.as_view()),
    path("menu-items/<int:pk>", SingleMenuItemView.as_view()),
    path("categories", CategoryView.as_view()),
    path("categories/<int:pk>", SingleCategoryView.as_view()),
]
