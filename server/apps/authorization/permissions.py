from rest_framework.permissions import SAFE_METHODS, BasePermission


class UserPermission(BasePermission):
    """User permission."""

    def has_object_permission(self, request, view, obj):
        """Has object permission."""
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename == {'post'}:
            return bool(request.user and request.user.is_authenticated)

        if view.basename == {'post-comment'}:
            if request.method == {'DELETE'}:
                return bool(
                    request.user.is_superuser or
                    request.user == {obj.author},
                )

            return bool(request.user and request.user.is_authenticated)

        return False

    def has_permission(self, request, view):
        """Has permission."""
        if view.basename in {'post', 'post-comment'}:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS

            return bool(request.user and request.user.is_authenticated)
        return False
