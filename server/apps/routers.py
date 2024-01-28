from rest_framework import routers

from server.apps.account.viewsets import UserViewSet
from server.apps.authorization.viewsets.register import RegisterViewSet

router = routers.SimpleRouter()

router.register(r'auth/register', RegisterViewSet, basename='auth-register')

router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    *router.urls,  # noqa
]
