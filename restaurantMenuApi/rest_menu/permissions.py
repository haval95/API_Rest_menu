from rest_framework import permissions


class ManagerOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="manager").exists()


class CustomerOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="customer").exists()
