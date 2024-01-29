from server.apps.account.models import User
from server.common.djangoabs.serializers import AbstractSeralizer


class UserSerializer(AbstractSeralizer):
    """User serializers."""

    class Meta:
        model = User
        fields = [  # noqa: WPS317
            'id', 'username', 'first_name',
            'last_name', 'bio', 'email',  # add avatar
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['is_active']
