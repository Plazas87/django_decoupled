"""Serializers module."""

from ....application.dtos import CategoryDTO, DocumentDTO, WorkspaceDTO
from ....application.interfaces import IDBSerializer
from .models import Category, Document, Workspace


class DocumentDBSerializer(IDBSerializer[Document, DocumentDTO]):
    """DocumentDBSerializer class."""

    def serialize(self, database_obj: Document) -> DocumentDTO:
        """Serialize a database object into a DocumentDTO."""
        return DocumentDTO(
            id=str(database_obj.id),
            text=database_obj.text,
            category_id=str(database_obj.category_id),
        )

    def deserialize(self, dto: DocumentDTO) -> Document:
        """Deserialize a DocumentDTO into a database instance."""
        return Document(
            id=dto.id,
            text=dto.text,
            category_id=dto.category_id,
        )


class CategoryDBSerializer(IDBSerializer[Category, CategoryDTO]):
    """CategoryDBSerializer class."""

    _document_serializer: IDBSerializer[Document, DocumentDTO]

    def __init__(
        self, document_serializer: IDBSerializer[Document, DocumentDTO]
    ) -> None:
        """Class constructor."""
        self._document_serializer = document_serializer

    def serialize(self, database_obj: Category) -> CategoryDTO:
        """Serialize a database object into a CategoryDTO."""
        return CategoryDTO(
            id=str(database_obj.id),
            name=database_obj.name,
            workspace_id=str(database_obj.workspace_id),
            documents=[
                self._document_serializer.serialize(database_obj=document)
                for document in database_obj.documents.all()
            ],
        )

    def deserialize(self, dto: CategoryDTO) -> Category:
        """Deserialize a CategoryDTO into a database instance."""
        return Category(id=dto.id, name=dto.name, workspace_id=dto.workspace_id)


class WorkspaceDBSerializer(IDBSerializer[Workspace, WorkspaceDTO]):
    """WorkspaceDBSerializer class."""

    _category_serializer: IDBSerializer[Category, CategoryDTO]

    def __init__(
        self,
        category_serializer: IDBSerializer[Category, CategoryDTO],
    ) -> None:
        """Class constructor."""
        self._category_serializer = category_serializer

    def serialize(self, database_obj: Workspace) -> WorkspaceDTO:
        """Serialize a database object into a WorkspaceDTO."""
        return WorkspaceDTO(
            id=str(database_obj.id),
            name=database_obj.name,
            owner=str(database_obj.owner_id),
            categories=[
                self._category_serializer.serialize(database_obj=workspace)
                for workspace in database_obj.categories.all()
            ],
            model_id=str(database_obj.model_id),
            metrics=database_obj.metrics,
        )

    def deserialize(self, dto: WorkspaceDTO) -> Workspace:
        """Deserialize a WorkspaceDTO into a database instance."""
        return Workspace(
            id=dto.id,
            name=dto.name,
            owner_id=dto.owner,
            model_id=dto.model_id,
            metrics=dto.metrics,
        )
