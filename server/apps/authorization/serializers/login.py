from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from server.apps.account.serializers import UserSerializer


class LoginSerializer(TokenObtainPairSerializer):
    """Login serializer for user."""

    def validate(self, attrs):
        """Validate data."""
        data = super().validate(attrs)  # noqa: WPS110

        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data
