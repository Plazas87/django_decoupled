"""django_decoupled dependency injection package."""


class DependencyInjectionError(Exception):
    """Base class for Dependency injection errors."""

    def __init__(self, message: str) -> None:
        """Class constructor."""
        self.message = message
        super().__init__(self.message)


class NoSuchHandlerError(DependencyInjectionError):
    """
    NoSuchHandler Error class.

    Raised when there is no available handlers to process the request.
    """
