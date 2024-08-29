from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class CustomPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_active

        if request.method == 'DELETE':
            return request.user.is_superuser

        if request.method in ['PATCH', 'PUT']:
            return request.user.is_staff

        return False