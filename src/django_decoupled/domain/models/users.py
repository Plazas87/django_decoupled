"""User domain models module."""
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ..exceptions.users import (
    UserEmailValidationError,
    UserNameValidationError,
    UserPasswordValidationError,
)


@dataclass(frozen=True)
class UserID:
    """UserID value object."""

    value: UUID

    @classmethod
    def from_string(cls, value: str) -> UserID:
        """Create a UserID instance from a uuid string."""
        uuid = UUID(value)

        return cls(value=uuid)

    def __str__(self) -> str:
        """Nice string representation."""
        return f"{self.__class__.__name__}({self.value})"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"{self.__class__.__name__}({self.value})"


@dataclass
class UserName:
    """UserName value object."""

    value: str

    def __post_init__(self):
        """Post init validation for texts."""
        if len(self.value) > 2000:
            raise UserNameValidationError("Max text lenght (characters): 2000")


@dataclass
class UserEmail:
    """UserEmail value object."""

    value: str

    def __post_init__(self):
        """Post init validation for texts."""
        if len(self.value) > 2000:
            raise UserEmailValidationError("Max text lenght (characters): 2000")


@dataclass
class UserPassword:
    """UserPassword value object."""

    value: str

    def __post_init__(self):
        """Post init validation for texts."""
        if len(self.value) > 2000:
            raise UserPasswordValidationError("Max text lenght (characters): 2000")


class User:
    """User model class."""

    id: UserID
    name: UserName
    email: UserEmail
    password: UserPassword
