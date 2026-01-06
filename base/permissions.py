from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to admin (staff) users.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )


'''class IsMember(BasePermission):
    """
    Allows access only to authenticated non-staff users (Members).
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            not request.user.is_staff
        )'''

class IsMember(BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Is authenticated?", request.user.is_authenticated)
        print("Is staff?", request.user.is_staff)
        return bool(
            request.user and
            request.user.is_authenticated and
            not request.user.is_staff
        )

