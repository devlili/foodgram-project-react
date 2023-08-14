from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Проверяет, является ли пользователь аутентифицирован
    в роли администратора или автора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_superuser
        )
