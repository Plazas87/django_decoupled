"""User domain models module."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from ..exceptions.users import (
    UserEmailValidationError,
    UserFirstNameValidationError,
    UserLastNameValidationError,
    UserPasswordValidationError,
    UserRolNotSupportedError,
)


class UserRolType(Enum):
    """UserRol Enum Types."""

    SUPERUSER = 0
    ADMIN = 1
    STANDART = 2


@dataclass(frozen=True)
class UserRol:
    """UserRol value object."""

    value: UserRolType

    @classmethod
    def from_string(cls, value: str) -> UserRol:
        """Create a UserRol instance from a string."""
        try:
            user_rol = UserRolType[value.upper()]

        except KeyError as err:
            raise UserRolNotSupportedError(message=str(err))

        return UserRol(value=user_rol)

    def __str__(self) -> str:
        """Nice string representation."""
        return f"{self.__class__.__name__}({self.value.name})"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"{self.__class__.__name__}({self.value})"


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
class UserFirstName:
    """UserFirstName value object."""

    value: str

    def __post_init__(self):
        """Post init validation for texts."""
        if len(self.value) > 2000:
            raise UserFirstNameValidationError("Max text lenght (characters): 2000")


class UserLastName:
    """UserLastName value object."""

    value: str

    def __post_init__(self):
        """Post init validation for texts."""
        if len(self.value) > 2000:
            raise UserLastNameValidationError("Max text lenght (characters): 2000")


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
    first_name: UserFirstName
    last_name: UserLastName
    rol: UserRol
    email: UserEmail
    password: UserPassword
