from rest_framework import filters, viewsets


class AbstractViewSet(viewsets.ModelViewSet):
    """Abstract View set."""

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'created_at']
    ordering = ['-updated_at']
