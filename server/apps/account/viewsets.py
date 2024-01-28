from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from server.apps.account.models import User
from server.apps.account.serializers import UserSelializer


class UserViewSet(viewsets.ModelViewSet):
    """Here description user view set."""

    http_method_names = ('patch', 'get')
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSelializer

    def get_queryset(self):
        """Get a list of all the users."""
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        """Method is used by the viewset to get one user."""
        object_user = User.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, object_user)
        return object_user
