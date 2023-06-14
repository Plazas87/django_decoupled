"""Repositories module."""
import uuid
from dataclasses import asdict
from typing import List
from uuid import UUID

from ....application.dtos import CategoryDTO, DocumentDTO, WorkspaceDTO
from ....application.exceptions import (
    WorkspaceAlreadyExistsError,
    WorkspaceDoesNotExistsError,
)
from ....application.interfaces import IDBSerializer, IFinder, IRepository
from .models import Category, Document, Workspace


class DjangoWorkspaceRepository(IRepository[WorkspaceDTO]):
    """DjangoWorkspaceRepository class."""

    _workspace_finder: IFinder[WorkspaceDTO]
    _workspace_serializer: IDBSerializer[Workspace, WorkspaceDTO]
    _category_serializer: IDBSerializer[Category, CategoryDTO]
    _document_serializer: IDBSerializer[Document, DocumentDTO]

    def __init__(
        self,
        workspace_finder: IFinder[WorkspaceDTO],
        workspace_serializer: IDBSerializer[Workspace, WorkspaceDTO],
        category_serializer: IDBSerializer[Category, CategoryDTO],
        document_serializer: IDBSerializer[Document, DocumentDTO],
    ) -> None:
        """Class constructor."""
        self._workspace_finder = workspace_finder
        self._workspace_serializer = workspace_serializer
        self._category_serializer = category_serializer
        self._document_serializer = document_serializer

    @staticmethod
    def generate_uuid() -> UUID:
        """Generate an uuid."""
        return uuid.uuid4()

    def save(self, workspace: WorkspaceDTO) -> None:
        """Save a workspace obj in the database."""
        if self._workspace_finder.exists(name=workspace.name, owner_id=workspace.owner):
            raise WorkspaceAlreadyExistsError(message=workspace.id)

        workspace_db = self._workspace_serializer.deserialize(workspace)
        workspace_db.save()

        categories: List[Category] = []
        documents: List[Document] = []

        for category in workspace.categories:
            categories.append(self._category_serializer.deserialize(category))
            for document in category.documents:
                documents.append(self._document_serializer.deserialize(document))

        Category.objects.bulk_create(categories)
        Document.objects.bulk_create(documents)

    def update(self, workspace: WorkspaceDTO) -> None:
        """Update a workspace object in the database."""
        if not self._workspace_finder.exists(
            name=workspace.name, owner_id=workspace.owner
        ):
            raise WorkspaceDoesNotExistsError(message=workspace.id)

        Workspace.objects.update_or_create(
            id=workspace.id,
            defaults={
                "name": workspace.name,
                "owner_id": workspace.owner,
                "model_id": workspace.model_id,
                "metrics": workspace.metrics,
            },
        )

        for category in workspace.categories:
            category_db, category_created = Category.objects.update_or_create(
                id=category.id,
                defaults={"name": category.name, "workspace_id": category.workspace_id},
            )

            if not category_created:
                category_db.documents.all().delete()

            documents = [
                Document(**asdict(document)) for document in category.documents
            ]
            Document.objects.bulk_create(documents)
