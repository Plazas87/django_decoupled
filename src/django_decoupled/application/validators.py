"""Validators module."""
from typing import Any

from ..domain.models import CategoryName, DocumentText, WorkspaceName
from .interfaces import IValidator


class DocumentTextValidator(IValidator):
    """DocumentTextValidator class."""

    @staticmethod
    def validate(value: Any) -> None:
        """Validate the Text of a Document."""
        DocumentText(value=value)


class CategoryNameValidator(IValidator):
    """CategoryNameValidator class."""

    @staticmethod
    def validate(value: Any) -> None:
        """Validate the Name of a Category."""
        CategoryName(value=value)


class WorksapceNameValidator(IValidator):
    """WorksapceNameValidator class."""

    @staticmethod
    def validate(value: Any) -> None:
        """Validate the Name of a Workspace."""
        WorkspaceName(value=value)


class WorkspaceFileValidator(IValidator):
    """WorkspaceFileValidator class."""

    @staticmethod
    def validate(value: Any) -> None:
        """Validate the name of a file dataset."""
        ### Performs validations related to the excel file
        print(f"Uploaded file: {value._name}")
