from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from server.apps.post.models import Post
from server.apps.post.serializers import PostSerializer
from server.common.djangoabs.viewsets import AbstractViewSet


class PostViewSet(AbstractViewSet):
    """Post view set."""

    http_method_names = ('post', 'get', 'put', 'delete')
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        """Method return all the posts."""
        return Post.objects.select_related('author').all()

    def get_object(self):
        """Method return a post object using p_id."""
        obj = Post.objects.get_object_by_public_id(  # noqa: WPS110
            self.kwargs['pk'],
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        """Create view."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        """Like post."""
        post = self.get_object()
        user = self.request.user

        user.like(post)

        serializer = self.serializer_class(post)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        """Remove like from post."""
        post = self.get_object()
        user = self.request.user

        user.remove_like(post)

        serializer = self.serializer_class(post)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
