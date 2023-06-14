"""Domain exceptions module."""


class DomainError(Exception):
    """Base class for Domain Exceptions."""


class DocumentTextValidationError(DomainError):
    """DocumentTextValidationError Error."""

    def __init__(self, message: str) -> None:
        """Class constructor."""
        self.message = message
        super().__init__(self.message)


class CategoryNameValidationError(DomainError):
    """CategoryNameValidationError Error."""

    def __init__(self, message: str) -> None:
        """Class constructor."""
        self.message = message
        super().__init__(self.message)


class WorkspaceNameValidationError(DomainError):
    """WorkspaceNameValidationError Error."""

    def __init__(self, message: str) -> None:
        """Class constructor."""
        self.message = message
        super().__init__(self.message)
