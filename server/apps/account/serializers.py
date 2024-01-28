from rest_framework import serializers

from server.apps.account.models import User


class UserSelializer(serializers.ModelSerializer):
    """User serializers."""

    id = serializers.UUIDField(
        source='public_id',
        read_only=True,
        format='hex',
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [  # noqa: WPS317
            'id', 'username', 'first_name',
            'last_name', 'bio', 'email',  # add avatar
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_field = ['is_active']
