from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings

from server.apps.account.serializers import UserSerializer


class LoginSerializer(TokenObtainPairSerializer):
    """Login serializer for user."""

    def validate(self, attrs):
        """Validate data."""
        print(f"Attempting login with data: {attrs}")
        
        try:
            data = super().validate(attrs)  # noqa: WPS110
        except TokenError as e:
            print(f'TokenError: {str(e)}')
            raise InvalidToken(str(e))
        
        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        print(f"Login successful, data: {data}")
        return data
