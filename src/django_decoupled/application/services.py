"""Application services module."""
import uuid
from typing import Dict, List, Optional, Set

from ..domain.models.workspaces import (
    Category,
    CategoryCollection,
    CategoryId,
    CategoryName,
    Document,
    DocumentCollection,
    DocumentId,
    DocumentText,
    Workspace,
    WorkspaceId,
    WorkspaceMetrics,
    WorkspaceModelId,
    WorkspaceName,
    WorkspaceOwnerId,
)
from .dtos import (
    CategoryDTO,
    DocumentDTO,
    FileCategory,
    FileDocument,
    FileWorkspace,
    WorkspaceDTO,
)
from .interfaces import IDomainSerializer, IFileProcessor, IFinder


class DocumentDomainSerializer(IDomainSerializer[Document, DocumentDTO]):
    """DocumentDomainSerializer class."""

    def serialize(self, domain_obj: Document) -> DocumentDTO:
        """Serialize a Domain instance into a DocumentDTO."""
        return DocumentDTO(
            id=str(domain_obj.id.value),
            text=domain_obj.text.value,
            category_id=str(domain_obj.category.value),
        )

    def deserialize(self, dto: DocumentDTO) -> Document:
        """Deserialize a DTO isntance into a Domain Document instance."""
        return Document(
            id=DocumentId.from_string(value=dto.id),
            text=DocumentText(value=dto.text),
            category_id=CategoryId.from_string(value=dto.category_id),
        )


class CategoryDomainSerializer(IDomainSerializer[Category, CategoryDTO]):
    """CategoryDomainSerializer class."""

    _document_serializer: IDomainSerializer[Document, DocumentDTO]

    def __init__(
        self, document_serializer: IDomainSerializer[Document, DocumentDTO]
    ) -> None:
        """Class constructor."""
        self._document_serializer = document_serializer

    def serialize(self, domain_obj: Category) -> CategoryDTO:
        """Serialize a Domain instance into a CategoryDTO."""
        return CategoryDTO(
            id=str(domain_obj.id.value),
            name=domain_obj.name.value,
            workspace_id=str(domain_obj.workspace.value),
            documents=[
                self._document_serializer.serialize(domain_obj=domain_document)
                for domain_document in domain_obj.documents.values()
            ],
        )

    def deserialize(self, dto: CategoryDTO) -> Category:
        """Deserialize a CategoryDTO instance into a Domain instance."""
        return Category(
            id=CategoryId.from_string(value=dto.id),
            name=CategoryName(value=dto.name),
            documents=DocumentCollection(
                items=[
                    self._document_serializer.deserialize(dto=document)
                    for document in dto.documents
                ]
            ),
            workspace_id=WorkspaceId.from_string(value=dto.workspace_id),
        )


class WorkspaceDomainSerializer(IDomainSerializer[Workspace, WorkspaceDTO]):
    """WorkspaceDomainSerializer class."""

    _category_serializer: IDomainSerializer[Category, CategoryDTO]

    def __init__(
        self, category_serializer: IDomainSerializer[Category, CategoryDTO]
    ) -> None:
        """Class constructor."""
        self._category_serializer = category_serializer

    def serialize(self, domain_obj: Workspace) -> WorkspaceDTO:
        """Serialize a database object into a DomainWorkspace."""
        return WorkspaceDTO(
            id=str(domain_obj.id.value),
            name=domain_obj.name.value,
            categories=[
                self._category_serializer.serialize(domain_obj=category)
                for category in domain_obj.categories.values()
            ],
            owner=str(domain_obj.owner.value),
            model_id=str(domain_obj.model_id.value)
            if domain_obj.model_id is not None
            else None,
            metrics=domain_obj.metrics.value,
        )

    def deserialize(self, dto: WorkspaceDTO) -> Workspace:
        """Deserialize a DTO isntance into a Domain instance."""
        return Workspace(
            id=WorkspaceId.from_string(dto.id),
            name=WorkspaceName(dto.name),
            categories=CategoryCollection(
                items=[
                    self._category_serializer.deserialize(dto=category_dto)
                    for category_dto in dto.categories
                ]
            ),
            owner_id=WorkspaceOwnerId.from_string(dto.owner),
            model_id=WorkspaceModelId(value=dto.model_id)
            if dto.model_id is not None
            else dto.model_id,
            metrics=WorkspaceMetrics(value=dto.metrics),
        )


class ExcelFileProcessor(IFileProcessor[Workspace, FileWorkspace, str]):
    """ExcelFileProcessor class."""

    _workspace_finder: IFinder[WorkspaceDTO]
    _serializer: IDomainSerializer[Workspace, WorkspaceDTO]
    _new_workspaces: Set[Workspace]
    _existing_workspaces: Set[Workspace]
    _data: Dict[str, Workspace]

    def __init__(
        self,
        workspace_finder: IFinder[WorkspaceDTO],
        serializer: IDomainSerializer[Workspace, WorkspaceDTO],
    ) -> None:
        """Class constructor."""
        self._workspace_finder = workspace_finder
        self._serializer = serializer
        self._new_workspaces = set()
        self._existing_workspaces = set()
        self._data = {}

    @property
    def new_objs(self):
        """Return new workspaces found within the Excel File."""
        return self._new_workspaces

    @property
    def existing_objs(self):
        """Return existing workspaces found within the Excel File."""
        return self._existing_workspaces

    def process(self, file_workspaces: Set[FileWorkspace], owner: str) -> None:
        """Process File Workspaces."""
        for file_workspace in file_workspaces:
            if self._workspace_finder.exists(name=file_workspace.name, owner_id=owner):
                self._existing_workspaces.add(
                    self._process_existing_workspace(
                        file_workspace=file_workspace, owner_id=owner
                    )
                )
                continue

            self._new_workspaces.add(
                self._workspace_to_domain(
                    file_workspace=file_workspace,
                    owner=owner,
                )
            )

        tmp_new_data = {
            workspace.name.value: workspace for workspace in self._new_workspaces
        }
        tmp_existing_data = {
            workspace.name.value: workspace for workspace in self._existing_workspaces
        }

        self._data = {**tmp_new_data, **tmp_existing_data}

    def get(self, name: str) -> Optional[Workspace]:
        """Return a workspace by name."""
        return self._data.get(name, None)

    def _process_existing_workspace(
        self, file_workspace: FileWorkspace, owner_id: str
    ) -> Workspace:
        """Build workspaces base on database existencies."""
        workspace = self._serializer.deserialize(
            dto=self._workspace_finder.get_by_name(
                name=file_workspace.name, owner_id=owner_id
            )
        )

        return Workspace(
            id=workspace.id,
            name=workspace.name,
            owner_id=workspace.owner,
            categories=CategoryCollection(
                self._process_existing_categories(
                    existing_categories=workspace.categories,
                    file_categories=file_workspace.categories,
                    workspace_id=str(workspace.id.value),
                )
            ),
        )

    def _process_existing_categories(
        self,
        existing_categories: CategoryCollection,
        file_categories: List[FileCategory],
        workspace_id: str,
    ) -> List[Category]:
        new_categories: Set[Category] = set()
        categories_to_be_updated: Set[Category] = set()

        existing_category_name_set = {
            existing_category.name.value
            for existing_category in existing_categories.values()
        }

        existing_category_name_map = {
            existing_category.name.value: existing_category
            for existing_category in existing_categories.values()
        }

        file_categories_name_map = {
            file_category.name: file_category for file_category in file_categories
        }
        file_categories_set = {file_category.name for file_category in file_categories}

        new_category_names_in_file = file_categories_set - existing_category_name_set
        existing_category_names_in_file = (
            file_categories_set - new_category_names_in_file
        )

        new_file_categories = {
            file_categories_name_map[new_category_name]
            for new_category_name in new_category_names_in_file
        }
        existing_file_categories = {
            file_categories_name_map[update_category_name]
            for update_category_name in existing_category_names_in_file
        }

        for new_file_category in new_file_categories:
            new_categories.add(
                self._category_to_domain(
                    file_category=new_file_category, workspace_id=workspace_id
                )
            )

        for existing_file_category in existing_file_categories:
            categories_to_be_updated.add(
                Category(
                    id=existing_category_name_map[existing_file_category.name].id,
                    name=CategoryName(value=existing_file_category.name),
                    workspace_id=WorkspaceId.from_string(value=workspace_id),
                    documents=DocumentCollection(
                        items=[
                            self._document_to_domain(
                                file_document=file_document,
                                category_id=str(
                                    existing_category_name_map[
                                        existing_file_category.name
                                    ].id.value
                                ),
                            )
                            for file_document in existing_file_category.documents
                        ]
                    ),
                )
            )

        return list(new_categories | categories_to_be_updated)

    def _workspace_to_domain(
        self,
        file_workspace: FileWorkspace,
        owner: str,
    ) -> Workspace:
        """Map external file instances to Domain instances."""
        workspace_id = WorkspaceId(value=uuid.uuid4())

        return Workspace(
            id=workspace_id,
            name=WorkspaceName(value=file_workspace.name),
            owner_id=WorkspaceOwnerId.from_string(value=owner),
            categories=CategoryCollection(
                items=[
                    self._category_to_domain(
                        file_category=file_category,
                        workspace_id=str(workspace_id.value),
                    )
                    for file_category in file_workspace.categories
                ]
            ),
        )

    def _category_to_domain(
        self, file_category: FileCategory, workspace_id: str
    ) -> Category:
        """Map external file instances to Domain instances."""
        category_id = CategoryId(value=uuid.uuid4())
        return Category(
            id=category_id,
            name=CategoryName(value=file_category.name),
            workspace_id=WorkspaceId.from_string(value=workspace_id),
            documents=DocumentCollection(
                items=[
                    self._document_to_domain(
                        file_document=file_document, category_id=str(category_id.value)
                    )
                    for file_document in file_category.documents
                ]
            ),
        )

    def _document_to_domain(
        self, file_document: FileDocument, category_id: str
    ) -> Document:
        """Map external file instances to Domain instances."""
        return Document(
            id=DocumentId(value=uuid.uuid4()),
            text=DocumentText(value=file_document.text),
            category_id=CategoryId.from_string(value=category_id),
        )
