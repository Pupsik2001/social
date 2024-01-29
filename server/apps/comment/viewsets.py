from django.http.response import Http404
from rest_framework import status
from rest_framework.response import Response

from server.apps.authorization.permissions import UserPermission
from server.apps.comment.models import Comment
from server.apps.comment.serializers import CommentSerializer
from server.common.djangoabs.viewsets import AbstractViewSet


class CommentViewSet(AbstractViewSet):
    """View for comment."""

    http_method_names = ('post', 'get', 'put', 'delete')
    permission_classes = (UserPermission,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Queryset for comment."""
        if self.request.user.is_superuser:
            return Comment.objects.all().select_related('post', 'author')

        post_pk = self.kwargs['post_pk']
        if post_pk is None:
            return Http404

        return Comment.objects.filter(post__public_id=post_pk).select_related('post', 'author')

    def get_object(self):
        """Get object comment."""
        obj = Comment.objects.get_object_by_public_id(
            self.kwargs['pk'],
        )
        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        """Create comment."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
