from typing import Final

from rest_framework import serializers

from server.apps.account.models import User
from server.apps.account.serializers import UserSerializer

_MAX_LENGTH_PASSWORD: Final = 128


class RegisterSerializer(UserSerializer):
    """Registration serializer for requests and uesr creation."""

    # Making sure the password is at least 8 characters long,
    # and no longer than 128
    password = serializers.CharField(
        max_length=_MAX_LENGTH_PASSWORD,
        min_length=8,
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        # List of all the fields that cn be included in a request or a response
        fields = [  # noqa: WPS 317
            'id', 'bio', 'email',
            'username', 'first_name', 'last_name',
            'password',
        ]

        def create(self, validated_data):
            """Use the 'create_user' method."""
            return User.objects.create_user(**validated_data)
