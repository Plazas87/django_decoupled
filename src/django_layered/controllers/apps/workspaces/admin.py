"""Workspaces admin module."""
from typing import TYPE_CHECKING

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from ....dependency_injection.containers import container
from .forms import CategoryForm, DocumentForm, WorkspaceForm
from .models import (
    Category,
    Document,
    Workspace,
)

if TYPE_CHECKING:
    from ....dependency_injection.dispatcher import Dispatcher

from ....application.commands import TrainWorkspaceCommand


class DocumentAdmin(admin.ModelAdmin):
    """DocumentAdmin class."""

    form = DocumentForm

    def get_queryset(self, request):
        """Filter the admin query set by User."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(category__workspace__owner=request.user)


class CategoryAdmin(admin.ModelAdmin):
    """CategoryAdmin class."""

    form = CategoryForm

    def get_queryset(self, request):
        """Filter the admin query set by User."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(workspace__owner=request.user)


class WorkspaceAdmin(admin.ModelAdmin):
    """WorkspaceAdmin class."""

    form = WorkspaceForm
    list_filter = (("owner", admin.RelatedOnlyFieldListFilter),)
    actions = ["train_workspaces"]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Filter the admin query set by User."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(owner=request.user)

    @admin.action(description="Train selected Workspaces")
    def train_workspaces(
        self,
        request: HttpRequest,
        queryset: QuerySet,
        dispatcher: "Dispatcher" = container.dispatcher,
    ) -> None:
        """
        Train selected workspaces.

        Args:
            request (HttpRequest): Django HttpReques
            queryset (Queryset): selected workspaces queryset
            dispatcher (Dispatcher, optional): command dispatcher. Defaults to container.dispatcher().
        """
        for workspace in queryset:
            train_workspace_command = TrainWorkspaceCommand(
                owner=str(request.user.id), workspace_id=str(workspace.id)
            )

            dispatcher.dispatch(command=train_workspace_command)


admin.site.register(Document, DocumentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
