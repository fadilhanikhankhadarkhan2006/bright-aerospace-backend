from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """Allows access only to users with role 'student'."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "student")


class IsCompany(permissions.BasePermission):
    """Allows access only to users with role 'company'."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "company")


class IsAdmin(permissions.BasePermission):
    """Allows access only to users with role 'admin'."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == "admin" or request.user.is_superuser or request.user.is_staff))
