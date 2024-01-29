from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from server.apps.authorization.serializers.login import LoginSerializer


class LoginViewSet(ViewSet):
    """Login view set."""

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """Create login view."""
        serializer = self.serializer_class(
            data=request.data,
        )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:  # noqa: WPS111
            raise InvalidToken(e.args[0])

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )
