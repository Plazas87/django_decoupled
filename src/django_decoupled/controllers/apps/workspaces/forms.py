"""Workspaces forms module."""
from typing import Any

from django import forms

from ....application.validators import (
    CategoryNameValidator,
    DocumentTextValidator,
    WorksapceNameValidator,
    WorkspaceFileValidator,
)
from ....infrastructure.persistence.workspaces.models import (
    Category,
    Document,
    Workspace,
)


class DocumentForm(forms.ModelForm):
    """DocumentForm class."""

    class Meta:
        """Meta class."""

        model = Document
        fields = ["text", "category"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Init method."""
        super().__init__(*args, **kwargs)
        self.fields["text"].validators = [DocumentTextValidator.validate]


class CategoryForm(forms.ModelForm):
    """CategoryForm class."""

    class Meta:
        """Meta class."""

        model = Category
        fields = ["name", "workspace"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Init method."""
        super().__init__(*args, **kwargs)
        self.fields["name"].validators = [CategoryNameValidator.validate]


class WorkspaceForm(forms.ModelForm):
    """WorkspaceForm class."""

    class Meta:
        """Meta class."""

        model = Workspace
        fields = ["name", "owner", "model_id", "metrics"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Init method."""
        super().__init__(*args, **kwargs)
        self.fields["name"].validators = [WorksapceNameValidator.validate]


class WorkspaceWithFileUploadForm(WorkspaceForm):
    """WorkspaceWithFileUploadForm class."""

    dataset = forms.FileField(
        validators=[WorkspaceFileValidator.validate], required=True
    )
