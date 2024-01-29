from typing import Any, Final

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from server.common.djangoabs.models import (
    AbstractIdTimedMixin,
    AbstractManager,
)

_USER_MAX_LENGTH: Final = 255


class UserManager(BaseUserManager['User'], AbstractManager):
    """User manager."""

    def create_user(
        self,
        username: str,
        email: str,
        password=None,
        **extra_fields: Any,
    ) -> 'User':
        """Create and return with an email number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')
        if password is None:
            raise TypeError('User must have an password.')

        user = User(
            username=username,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username: str,
        email: str,
        password: str,
        **extra_fields: Any,
    ) -> 'User':
        """Create and return a `User` with superuser (admin) permissions."""
        if username is None:
            raise TypeError('Superusers must have an username.')
        if email is None:
            raise TypeError('Superuser must have an email.')
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db, update_fields=['is_superuser', 'is_staff'])
        return user


class User(AbstractBaseUser, PermissionsMixin, AbstractIdTimedMixin):
    """User model, use AbstractBaseUser abstact model."""

    username = models.CharField(
        db_index=True,
        max_length=_USER_MAX_LENGTH,
        unique=True,
    )
    first_name = models.CharField(max_length=_USER_MAX_LENGTH)
    last_name = models.CharField(max_length=_USER_MAX_LENGTH)
    email = models.EmailField(db_index=True, unique=True)

    bio = models.TextField(default='')
    # add 'avatar imagefield'

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # noqa: WPS110

    USERNAME_FIELD = 'email'  # noqa: WPS115
    REQUIRED_FIELDS = ['username']  # noqa: WPS115

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        """Return email users."""
        return '{0}'.format(self.email)

    @property
    def name(self):
        """Return users name and second name."""
        return '{0} {1}'.format(self.first_name, self.last_name)
