"""Commands module."""
from dataclasses import dataclass
from typing import Optional

from ..dependency_injection.dispatcher import Command


@dataclass
class CreateOrUpdateWorkspaceFromUploadExcelFileCommand(Command):
    """CreateOrUpdateWorkspaceFromUploadExcelFileCommand Command."""

    file_bytes: bytes
    owner: str


@dataclass
class CreateWorkspaceAndAddDataFromFileCommand(Command):
    """CreateWorkspaceAndAddDataFromFileCommand Command."""

    workspace_name: str
    file_bytes: bytes
    owner_id: str


@dataclass
class TrainWorkspaceCommand(Command):
    """TrainWorkspaceCommand Command."""

    workspace_id: str
    owner: str


@dataclass
class CreateWorkspaceCommand(Command):
    """CreateWorkspaceCommand class."""

    name: str
    owner_id: str
    type: Optional[str] = None


@dataclass
class WorkspaceMetricsCommand(Command):
    """WorkspaceMetricsCommand class."""

    workspace_id: str
    owner: str
