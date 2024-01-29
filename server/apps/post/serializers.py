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

    class Meta:
        model = Post
        fields = ['id', 'author', 'body', 'edited', 'created_at', 'updated_at']
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
