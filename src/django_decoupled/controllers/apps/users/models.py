"""User model module."""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import UserManager


class User(AbstractUser):
    """Custom User model."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    username = None
    email = models.EmailField(_("email address"), unique=True, null=False)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        """User Meta class."""

        verbose_name = _("User")
        verbose_name_plural = _("users")
        ordering = ["email"]
        app_label = "users"
