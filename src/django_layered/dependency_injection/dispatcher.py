"""Dispatcher module."""
from __future__ import annotations

import logging
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Generic, Type, TypeVar

from .expections import NoSuchHandlerError

logger = logging.getLogger(__name__)


T = TypeVar("T", covariant=True)


class Command(Generic[T]):  # pylint: disable=too-few-public-methods
    """Command class."""


class Handler(Generic[T]):  # pylint: disable=too-few-public-methods
    """Handler class."""

    @abstractmethod
    def handle(self, command: Command) -> T:
        """Handle a command."""


class NullHandler(Handler):
    """Null handler."""

    def handle(self, command: Command) -> None:
        """Handle returning none."""
        return None


@dataclass
class Dispatcher:
    """Command dispatcher."""

    _handlers: Dict[Type[Command], Handler]

    def __init__(self, handlers: Dict[Type[Command], Handler]) -> None:
        """Class constructor."""
        self._handlers = handlers

    def dispatch(self, command: Command) -> Any:
        """Dispatch the command to his handler."""
        try:
            command_handler = self._handlers[command.__class__]
        except NoSuchHandlerError:
            command_handler = NullHandler()

        return command_handler.handle(command)
