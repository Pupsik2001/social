from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.apps.account.models import User
from server.apps.account.serializers import UserSerializer
from server.apps.post.models import Post
from server.common.djangoabs.serializers import AbstractSeralizer


class PostSerializer(AbstractSeralizer):
    """Post serializer."""

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='public_id',
    )
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'body',
            'edited',
            'liked',
            'likes_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['edited']

    def validate_author(self, value):  # noqa: WPS110
        """Check and validate author."""
        if self.context['request'].user != value:
            raise ValidationError("You can't create a post for another user.")
        return value

    def to_representation(self, instance):
        """Representation author."""
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(
            rep['author'],
        )
        rep['author'] = UserSerializer(author).data

        return rep

    def update(self, instance, validated_data):
        """Update post."""
        if not instance.edited:
            validated_data['edited'] = True

        return super().update(instance, validated_data)

    def get_liked(self, instance):  # noqa: WPS615
        """Get liked post."""
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous:
            return False

        return request.user.has_liked(instance)

    def get_likes_count(self, instance):  # noqa: WPS615
        """Find out how many likes."""
        return instance.liked_by.count()
