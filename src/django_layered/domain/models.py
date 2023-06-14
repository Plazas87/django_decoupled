"""Classify models module."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from .exceptions import (
    CategoryNameValidationError,
    DocumentTextValidationError,
    WorkspaceNameValidationError,
)

T = TypeVar("T")
K = TypeVar("K")


@dataclass(frozen=True)
class DocumentId:
    """DocumentId value object."""

    value: UUID

    @classmethod
    def from_string(cls, value: str) -> DocumentId:
        """Create a DocumentId instance from a uuid string."""
        uuid = UUID(value)

        return cls(value=uuid)

    def __str__(self) -> str:
        """Nice string representation."""
        return f"{self.__class__.__name__}({self.value})"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"{self.__class__.__name__}({self.value})"


@dataclass
class DocumentText:
    """DocumentText value object."""

    value: str

    def __post_init__(self):
        """Post init validation for texts."""
        if len(self.value) > 2000:
            raise DocumentTextValidationError("Max text lenght (characters): 2000")


@dataclass(frozen=True)
class WorkspaceId:
    """WorkspaceId value object."""

    value: UUID

    @classmethod
    def from_string(cls, value: str) -> WorkspaceId:
        """Create a WorkspaceId instance from a uuid string."""
        uuid = UUID(value)

        return cls(value=uuid)

    def __str__(self) -> str:
        """Nice string representation."""
        return f"{self.__class__.__name__}({self.value})"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"{self.__class__.__name__}({self.value})"


@dataclass(frozen=True)
class WorkspaceOwnerId:
    """OwnerId value object."""

    value: UUID

    @classmethod
    def from_string(cls, value: str) -> WorkspaceOwnerId:
        """Create a WorkspaceOwnerId instance from a uuid string."""
        uuid = UUID(value)

        return cls(value=uuid)

    def __str__(self) -> str:
        """Nice string representation."""
        return f"{self.__class__.__name__}({self.value})"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"{self.__class__.__name__}({self.value})"


@dataclass(frozen=True)
class WorkspaceModelId:
    """WorkspaceModelId value object."""

    value: str

    def __str__(self) -> str:
        """Nice string representation."""
        return f"{self.__class__.__name__}({self.value})"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"{self.__class__.__name__}({self.value})"


@dataclass
class WorkspaceName:
    """WorkspaceName value object."""

    value: str

    def __post_init__(self):
        """Post init validation for texts."""
        if len(self.value) > 100:
            raise WorkspaceNameValidationError("Max text lenght (characters): 200")


@dataclass
class WorkspaceMetrics:
    """WorkspaceMetrics value object."""

    value: Dict[str, Any]


@dataclass(frozen=True)
class CategoryId:
    """CategoryId value object."""

    value: UUID

    @classmethod
    def from_string(cls, value: str) -> CategoryId:
        """Create a CategoryId instance from a uuid string."""
        uuid = UUID(value)

        return cls(value=uuid)

    def __str__(self) -> str:
        """Nice string representation."""
        return f"{self.__class__.__name__}({self.value})"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"{self.__class__.__name__}({self.value})"


@dataclass
class CategoryName:
    """CategoryName value object."""

    value: str

    def __post_init__(self):
        """Post init validation for texts."""
        if len(self.value) > 100:
            raise CategoryNameValidationError("Max text lenght (characters): 200")


class Collection(Generic[K, T]):
    """Collection base interface."""

    _data: Dict[K, T] = {}

    def __init__(self, items: Optional[List[T]] = None) -> None:
        """Class constructor."""
        self._data = {} if items is None else {item.id: item for item in items}  # type: ignore

    def add(self, item: T) -> None:
        """
        Add a Item to the collection.

        Args:
            item (T): Item to be added

        Raises
            DocumentAlreadyExistError: raise when the item already exists in the collection.
        """
        if self._exists(id=item.id):  # type: ignore
            raise Exception(f"The item with ID '{item.id}' already exists in the collection.")  # type: ignore

        self._data[item.id] = item  # type: ignore

    def update(self, item: T) -> None:
        """
        Update a Document in the collection.

        Args:
            item (T): item to be updated

        Raises
            DocumentDoesNoExistError: raised when the item to update does not
            exist within the collection.
        """
        if not self._exists(id=item.id):  # type: ignore
            raise Exception(f"The item with ID '{item.id.value}' does not exist.")  # type: ignore

        self._data.update({item.id: item})  # type: ignore

    def remove(self, id: K) -> None:
        """
        Remove an item from the collection.

        Args:
            id (K): item ID

        Raises
            DocumentDoesNoExistError: raised when the item to update does not
            exist within the collection.
        """
        if not self._exists(id=id):
            raise Exception(f"The item with ID '{id.value}' does not exist.")  # type: ignore

        self._data.pop(id)

    def get(self, id: K) -> T:
        """
        Return a item by ID.

        Args:
            id (K): item ID to look for

        Returns
            K: an item.
        """
        if not self._exists(id=id):
            raise Exception(f"The item with ID '{id.value}' does not exist.")  # type: ignore

        return self._data[id]

    def values(self):
        """Return the collection values."""
        for item in self._data.values():
            yield item

    def _exists(self, id: K) -> bool:
        """
        Check if a item already exists within the collection.

        Args:
            id (K): item ID.

        Returns
            bool: True if the item exists, false otherwise.
        """
        if id not in self._data.keys():
            return False

        return True


class Workspace:
    """Domain Workspace model class."""

    _id: WorkspaceId
    _name: WorkspaceName
    _categories: CategoryCollection
    _owner_id: WorkspaceOwnerId
    _metrics: WorkspaceMetrics
    _model_id: Optional[WorkspaceModelId] = None

    def __init__(
        self,
        id: WorkspaceId,
        name: WorkspaceName,
        categories: CategoryCollection,
        owner_id: WorkspaceOwnerId,
        metrics: WorkspaceMetrics = WorkspaceMetrics(value={}),
        model_id: Optional[WorkspaceModelId] = None,
    ) -> None:
        """Class constructor."""
        self._id = id
        self._name = name
        self._categories = categories
        self._owner_id = owner_id
        self._model_id = model_id
        self._metrics = metrics

    @property
    def id(self) -> WorkspaceId:
        """
        Return the Workspace ID.

        Returns
            WorkspaceId: WorkspaceId instance.
        """
        return self._id

    @property
    def name(self) -> WorkspaceName:
        """
        Return the Workspace name.

        Returns
            WorkspaceName: WorkspaceName instance.
        """
        return self._name

    @property
    def owner(self) -> WorkspaceOwnerId:
        """
        Return the Owner ID.

        Returns
            OwnerId: OwnerId instance.
        """
        return self._owner_id

    @property
    def categories(self) -> CategoryCollection:
        """
        Return the categories of the workspace.

        Returns
            categories: categories collection.
        """
        return self._categories

    @property
    def model_id(self) -> Optional[WorkspaceModelId]:
        """
        Return the model ID for the workspace.

        Returns
            WorkspaceModelId: WorkspaceModelId instance
        """
        return self._model_id

    @property
    def metrics(self) -> WorkspaceMetrics:
        """
        Return report field of the worksapce.

        Returns
            WorkspaceMetrics: WorkspaceMetrics instance
        """
        return self._metrics

    def add_category(self, category: Category) -> None:
        """Add a Category to the workspace."""
        self._categories.add(item=category)

    def add_document(self, document: Document) -> None:
        """Add a Category to the workspace."""
        category = self._categories.get(id=document.category)
        category.documents.add(item=document)

    def set_model_id(self, model_id: str) -> None:
        """
        Set the model ID for a workspace.

        Args:
            model_id (str): model id
        """
        self._model_id = WorkspaceModelId(value=model_id)

    def set_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Set the metric for the workspace.

        Args:
            metrics (Dict[str, Any]): metrics
        """
        self._metrics = WorkspaceMetrics(value=metrics)

    def __str__(self) -> str:
        """Nice string representation."""
        return (
            f"{self.__class__.__name__}(id={str(self._id.value)}, "
            f"name={self._name.value}, categories={self._categories}')"
        )

    def __repr__(self) -> str:
        """Nice object representation."""
        return (
            f"{self.__class__.__name__}(id={str(self._id.value)}, "
            f"name={self._name.value}, categories={self._categories}')"
        )


class Category:
    """Category model."""

    _id: CategoryId
    _name: CategoryName
    _workspace_id: WorkspaceId
    _documents: DocumentCollection

    def __init__(
        self,
        id: CategoryId,
        name: CategoryName,
        workspace_id: WorkspaceId,
        documents: DocumentCollection,
    ) -> None:
        """Class constructor."""
        self._id = id
        self._name = name
        self._documents = documents
        self._workspace_id = workspace_id

    @property
    def id(self) -> CategoryId:
        """
        Return the Category ID.

        Returns
            CategoryId: CategoryId instance.
        """
        return self._id

    @property
    def name(self) -> CategoryName:
        """
        Return the Category name.

        Returns
            CategoryName: CategoryName instance.
        """
        return self._name

    @property
    def documents(self) -> DocumentCollection:
        """
        Return the document collection.

        Returns
            DocumentCollection: DocumentCollection instance.
        """
        return self._documents

    @property
    def workspace(self) -> WorkspaceId:
        """
        Return the workspace.

        Returns
            Workspace: Workspace instance.
        """
        return self._workspace_id

    def __str__(self) -> str:
        """Nice string representation."""
        return (
            f"{self.__class__.__name__}(id={str(self._id.value)}, "
            f"name={self._name.value}, workspace={self.workspace}, documents={self._documents})"
        )

    def __repr__(self) -> str:
        """Nice object representation."""
        return (
            f"{self.__class__.__name__}(id={str(self._id.value)}, "
            f"name='{self._name.value}, workspace={self.workspace.value}, documents={self._documents}')"
        )


class CategoryCollection(Collection[CategoryId, Category]):
    """Category collection."""

    def __str__(self) -> str:
        """Nice string representation."""
        return f"{list(self._data.values())}"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"{list(self._data.values())}"


class Document:
    """Document model."""

    _id: DocumentId
    _text: DocumentText
    _category_id: CategoryId

    def __init__(
        self, id: DocumentId, text: DocumentText, category_id: CategoryId
    ) -> None:
        """Class constructor."""
        self._id = id
        self._text = text
        self._category_id = category_id

    @property
    def id(self) -> DocumentId:
        """
        Return the document ID.

        Returns
            DocumentId: DocumentId instance.
        """
        return self._id

    @property
    def text(self) -> DocumentText:
        """
        Return the document text.

        Returns
            DocumentId: DocumentText instance.
        """
        return self._text

    @property
    def category(self) -> CategoryId:
        """
        Return the document text.

        Returns
            DocumentId: DocumentText instance.
        """
        return self._category_id

    def update_text(self, text: DocumentText) -> None:
        """Update the text."""
        self._text = text

    def __str__(self) -> str:
        """Nice string representation."""
        return f"{self.__class__.__name__}(id={str(self._id.value)}, text='{self._text.value}')"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"{self.__class__.__name__}(id={str(self._id.value)}, text='{self._text.value}')"


class DocumentCollection(Collection[DocumentId, Document]):
    """Document collection."""

    def __str__(self) -> str:
        """Nice string representation."""
        return f"{list(self._data.values())}"

    def __repr__(self) -> str:
        """Nice object representation."""
        return f"{list(self._data.values())}"
