from rest_framework import status
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
        obj = Post.objects.get_object_by_public_id(  # noqa
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
