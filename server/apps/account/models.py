import textwrap
from typing import Final
from uuid import uuid4

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404

_USER_MAX_LENGTH: Final = 255


class UserManager(BaseUserManager):
    """User manager."""

    def get_object_by_public_id(self, public_id):
        """Get users by public id."""
        try:  # noqa: WPS229
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

    def create_user(self, username, email, password=None, **kwargs):
        """Create and return with an email number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')
        if password is None:
            raise TypeError('User must have an password.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **kwargs):
        """Create and return a `User` with superuser (admin) permissions."""
        if username is None:
            raise TypeError('Superusers must have an username.')
        if email is None:
            raise TypeError('Superuser must have an email.')
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model, use AbstractBaseUser abstact model."""

    public_id = models.UUIDField(
        db_index=True,
        unique=True,
        default=uuid4,
        editable=False,
    )

    username = models.CharField(
        db_index=True,
        max_length=_USER_MAX_LENGTH,
        unique=True,
    )
    first_name = models.CharField(max_length=_USER_MAX_LENGTH)
    last_name = models.CharField(max_length=_USER_MAX_LENGTH)
    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        """Return email users."""
        return textwrap.wrap(self.email)

    @property
    def name(self):
        """Return users name and second name."""
        return '{0} {1}'.format(self.name, self.last_name)
