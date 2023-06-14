"""Workspace models module."""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Document(models.Model):
    """Document model class."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    text = models.TextField(_("text"), null=False, blank=False)

    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="documents"
    )

    class Meta:
        """Document Meta class."""

        verbose_name = _("Document")
        verbose_name_plural = _("documents")
        ordering = ["text"]
        app_label = "workspaces"

    def __str__(self) -> str:
        """Nice object string representation."""
        return f"{self.text}"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"Document(id={self.id}, text={self.text})"


class Category(models.Model):
    """Category model class."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    name = models.CharField(_("name"), max_length=150, null=False, blank=False)

    workspace = models.ForeignKey(
        "Workspace", on_delete=models.CASCADE, related_name="categories"
    )

    class Meta:
        """Category Meta class."""

        verbose_name = _("Category")
        verbose_name_plural = _("categories")
        ordering = ["name"]
        app_label = "workspaces"

    def __str__(self) -> str:
        """Nice object string representation."""
        return f"{self.name}"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"Category(id={self.id}, text={self.name})"


class Workspace(models.Model):
    """Workspace model class."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    name = models.CharField(_("name"), max_length=150, null=False, blank=False)

    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="workspaces"
    )

    model_id = models.CharField(_("model_id"), max_length=200, null=True, blank=True)

    metrics = models.JSONField(_("metrics"), default=dict, null=True, blank=True)

    class Meta:
        """Workspace Meta class."""

        verbose_name = _("Workspace")
        verbose_name_plural = _("workspaces")
        ordering = ["name"]
        app_label = "workspaces"

    def __str__(self) -> str:
        """Nice object string representation."""
        return f"{self.name}"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"Workspace(id={self.id}, text={self.name})"
