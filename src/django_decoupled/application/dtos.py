"""Data transfer object module."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union


@dataclass
class UserDTO:
    """UserDTO class."""

    id: str
    first_name: str
    last_name: str
    rol: str
    email: str
    password: Optional[str] = None


@dataclass
class DocumentDTO:
    """DocumentDTO."""

    id: str
    text: str
    category_id: str


@dataclass
class CategoryDTO:
    """CategoryDTO."""

    id: str
    name: str
    workspace_id: str
    documents: List[DocumentDTO]


@dataclass
class WorkspaceDTO:
    """WorkspaceDTO."""

    id: str
    name: str
    categories: List[CategoryDTO]
    owner: str
    model_id: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FileDocument:
    """DocumentDTO."""

    text: str

    def __eq__(self, value: object) -> bool:
        """Override the equal method for this class."""
        return isinstance(value, FileDocument) and self.text == value.text

    def __hash__(self) -> int:
        """Override the hash method for this class."""
        return hash((self.text,))


@dataclass
class FileCategory:
    """CategoryDTO."""

    name: str
    documents: List[FileDocument]

    def __eq__(self, value: object) -> bool:
        """Override the equal method for this class."""
        return isinstance(value, FileCategory) and self.name == value.name

    def __hash__(self) -> int:
        """Override the hash method for this class."""
        return hash((self.name,))


@dataclass
class FileWorkspace:
    """WorkspaceDTO."""

    name: str
    categories: List[FileCategory]

    def __eq__(self, value: object) -> bool:
        """Override the equal method for this class."""
        return isinstance(value, FileWorkspace) and self.name == value.name

    def __hash__(self) -> int:
        """Override the hash method for this class."""
        return hash((self.name,))


@dataclass(frozen=True)
class HTTPRequest:
    """Request data transfer object."""

    method: str
    url: str
    body: Optional[Union[Dict[str, Any], List[Any]]] = None
    headers: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class HTTPResponse:
    """ExecutionResponse data transfer object."""

    status_code: int
    headers: Dict[str, str]
    body: Dict[str, Any]


@dataclass(frozen=True)
class TrainingResponse:
    """Train Response."""

    model_id: Optional[str]
    success: bool
    errors: Optional[str]


@dataclass(frozen=True)
class TrainDataSet:
    """Train a text classifier."""

    texts: List[str]
    classes: List[str]
