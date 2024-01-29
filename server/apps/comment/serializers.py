from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.apps.account.models import User
from server.apps.account.serializers import UserSerializer
from server.apps.comment.models import Comment
from server.apps.post.models import Post
from server.common.djangoabs.serializers import AbstractSeralizer


class CommentSerializer(AbstractSeralizer):
    """Comment serializer."""

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='public_id',
    )
    post = serializers.SlugRelatedField(
        queryset=Post.objects.all(),
        slug_field='public_id',
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'body',
            'edited',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['edited']

    def to_representation(self, instance):
        """Representation."""
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep['author'])
        rep['author'] = UserSerializer(author).data

        return rep

    def validate_post(self, value):
        """Validate post."""
        if self.instance:
            return self.instance.post
        return value

    def update(self, instance, validated_data):
        """Method update comment."""
        if not instance.edited:
            validated_data['edited'] = True
        return super().update(instance, validated_data)
