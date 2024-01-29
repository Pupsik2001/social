from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermission(BasePermission):
    """User permission."""

    def has_object_permission(self, request, view, obj):
        """Has object permission."""
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ['post']:
            return bool(request.user and request.user.is_authenticated)
        return False

    def has_permission(self, request, view):
        """Hasd permission."""
        if view.basename is ['post']:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS

            return bool(request.user and request.user.is_authenticated)
        return False
