"""Domain exceptions package."""


class DomainError(Exception):
    """Base class for Domain Exceptions."""

    def __init__(self, message: str) -> None:
        """Class constructor."""
        self.message = message
        super().__init__(self.message)
