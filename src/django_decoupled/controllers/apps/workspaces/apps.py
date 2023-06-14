"""Workspace app config module."""
from django.apps import AppConfig


class WorkspacesConfig(AppConfig):
    """WorkspacesConfig class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_decoupled.controllers.apps.workspaces"
    verbose_name = "Workspaces"
    label = "workspaces"
