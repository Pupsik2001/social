from django.db import models

from server.common.djangoabs.models import (
    AbstractIdTimedMixin,
    AbstractManager,
)


class CommentManager(AbstractManager):
    """Comment manager."""


class Comment(AbstractIdTimedMixin):
    """Comment class."""

    post = models.ForeignKey(
        'post.Post',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
    )
    body = models.TextField(default='')
    edited = models.BooleanField(default=False)

    objects = CommentManager()

    def __str__(self):
        """Method return self name."""
        return '{0}'.format(self.author.name)
