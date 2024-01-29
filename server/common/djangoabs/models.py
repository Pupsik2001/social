from uuid import uuid4

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class AbstractManager(models.Manager):
    """Abstract manager."""

    def get_object_by_public_id(self, public_id):
        """Function for get object by id."""
        try:  # noqa: WPS229
            instance = self.get(public_id=public_id)
            return instance  # noqa: WPS331
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404


class AbstractIdTimedMixin(models.Model):
    """Adding utility fields for different models."""

    public_id = models.UUIDField(
        db_index=True,
        unique=True,
        default=uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AbstractManager()  # noqa: WPS110

    class Meta:
        abstract = True
