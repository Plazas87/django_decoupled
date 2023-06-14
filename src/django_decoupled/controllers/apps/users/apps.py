"""User app config module."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """UsersConfig class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_decoupled.controllers.apps.users"
    verbose_name = "Users"
