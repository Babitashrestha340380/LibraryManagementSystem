from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Allows access only to admin users (staff).
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class IsMember(BasePermission):
    """
    Allows access only to non-admin authenticated users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_staff)
