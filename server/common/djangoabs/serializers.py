from rest_framework import serializers


class AbstractSeralizer(serializers.ModelSerializer):
    """Abstract serializer."""

    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
