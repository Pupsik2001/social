from rest_framework import routers

from server.apps.account.viewsets import UserViewSet
from server.apps.authorization.viewsets import (
    LoginViewSet,
    RegisterViewSet,
    RefreshViewSet,
)
from server.apps.post.viewsets import PostViewSet

router = routers.SimpleRouter()

# AUTH
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

# POST
router.register(r'post', PostViewSet, basename='post')

# USER
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    *router.urls,  # noqa
]
