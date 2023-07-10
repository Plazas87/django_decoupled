"""User model exceptions."""

from . import DomainError


class UserFirstNameValidationError(DomainError):
    """UserFirstNameValidationError exception."""


class UserLastNameValidationError(DomainError):
    """UserLastNameValidationError exception."""


class UserEmailValidationError(DomainError):
    """UserEmailValidation exception."""


class UserPasswordValidationError(DomainError):
    """UserPasswordValidation exception."""


class UserRolNotSupportedError(DomainError):
    """UserRolNotSupported exception."""
