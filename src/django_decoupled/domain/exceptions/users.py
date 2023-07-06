"""User model exceptions."""

from . import DomainError


class UserNameValidationError(DomainError):
    """UserNameValidation exception."""


class UserEmailValidationError(DomainError):
    """UserEmailValidation exception."""


class UserPasswordValidationError(DomainError):
    """UserPasswordValidation exception."""
