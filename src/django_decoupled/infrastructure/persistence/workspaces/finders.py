"""Finders module."""
from typing import List, Optional

from django_decoupled.application.dtos import CategoryDTO, DocumentDTO, WorkspaceDTO
from django_decoupled.application.interfaces import IDBSerializer, IFinder

from .models import Category, Document, Workspace


class DjangoWorkspaceFinder(IFinder[WorkspaceDTO]):
    """DjangoWorkspaceFinder class."""

    _workspace_serializer: IDBSerializer[Workspace, WorkspaceDTO]

    def __init__(
        self,
        workspace_serializer: IDBSerializer[Workspace, WorkspaceDTO],
    ) -> None:
        """Class constructor."""
        self._workspace_serializer = workspace_serializer

    def get(self, id: str, owner_id: str) -> Optional[WorkspaceDTO]:
        """Get all available worksapaces by ID."""
        wrokspace = Workspace.objects.filter(id=id, owner=owner_id).first()

        return (
            self._workspace_serializer.serialize(database_obj=wrokspace)
            if wrokspace is not None
            else None
        )

    def get_by_name(self, name: str, owner_id: str) -> Optional[WorkspaceDTO]:
        """Get a Workspace by name."""
        wrokspace = Workspace.objects.filter(name=name, owner=owner_id).first()

        return (
            self._workspace_serializer.serialize(database_obj=wrokspace)
            if wrokspace is not None
            else None
        )

    def get_all(self, owner_id: str) -> List[WorkspaceDTO]:
        """Get all workspaces by onwer ID."""
        workspaces = Workspace.objects.filter(owner=owner_id)

        return [
            self._workspace_serializer.serialize(database_obj=workspace)
            for workspace in workspaces
        ]

    def exists(self, name: str, owner_id) -> bool:
        """Check id the object already existe in the database."""
        if Workspace.objects.filter(name=name, owner_id=owner_id).exists():
            return True

        return False


class DjangoCategoryFinder(IFinder[CategoryDTO]):
    """DjangoCategoryFinder class."""

    _category_serializer: IDBSerializer[Category, CategoryDTO]

    def __init__(
        self,
        category_serializer: IDBSerializer[Category, CategoryDTO],
    ) -> None:
        """Class constructor."""
        self._category_serializer = category_serializer

    def get(self, name: str, owner_id: str) -> Optional[CategoryDTO]:
        """Get a Category by name."""
        category = Category.objects.filter(name=name, workspace__owner=owner_id).first()

        return (
            self._category_serializer.serialize(database_obj=category)
            if category is not None
            else None
        )

    def exists(self, name: str, owner_id: str) -> bool:
        """Check id the object already existe in the database."""
        if Category.objects.filter(name=name, owner__id=owner_id).exists():
            return True

        return False

    def get_all(self, owner_id: str) -> List[CategoryDTO]:
        """Get all Categories by onwer ID."""
        categories = Category.objects.filter(workspace__owner=owner_id)

        return [
            self._category_serializer.serialize(database_obj=category)
            for category in categories
        ]


class DjangoDocumentFinder(IFinder[DocumentDTO]):
    """DjangoDocumentFinder class."""

    _document_serializer: IDBSerializer[Document, DocumentDTO]

    def __init__(
        self,
        document_serializer: IDBSerializer[Document, DocumentDTO],
    ) -> None:
        """Class constructor."""
        self._document_serializer = document_serializer

    def get_category(self, name: str, owner_id) -> Optional[DocumentDTO]:
        """Get a Document by te."""
        category = Document.objects.filter(name=name, workspace__owner=owner_id).first()

        return (
            self._document_serializer.serialize(database_obj=category)
            if category is not None
            else None
        )

    def exists(self, name: str, owner_id) -> bool:
        """Check id the object already existe in the database."""
        if Document.objects.filter(name=name, owner_id=owner_id).exists():
            return True

        return False

    def get_all(self, owner_id: str) -> List[DocumentDTO]:
        """Get all workspaces by onwer ID."""
        workspaces = Document.objects.filter(owner=owner_id)

        return [
            self._document_serializer.serialize(database_obj=workspace)
            for workspace in workspaces
        ]
