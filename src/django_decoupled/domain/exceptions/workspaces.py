"""Domain exceptions module."""

from . import DomainError


class DocumentTextValidationError(DomainError):
    """DocumentTextValidationError Error."""


class CategoryNameValidationError(DomainError):
    """CategoryNameValidationError Error."""


class WorkspaceNameValidationError(DomainError):
    """WorkspaceNameValidationError Error."""
