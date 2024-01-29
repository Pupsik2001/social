from django.db import models

from server.common.djangoabs.models import (
    AbstractIdTimedMixin,
    AbstractManager,
)


class PostManager(AbstractManager):
    """Post manager."""


# TODO: add in later description
class Post(AbstractIdTimedMixin):
    """Post models."""

    author = models.ForeignKey(
        to='account.User',
        on_delete=models.CASCADE,
    )
    body = models.TextField(default='')
    edited = models.BooleanField(default=False)

    objects = PostManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """Method str."""
        return '{0}'.format(self.author.name)

