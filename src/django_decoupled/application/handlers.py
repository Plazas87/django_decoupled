"""Train handle module."""
import logging
from dataclasses import asdict
from typing import Any, Dict, Optional

from django_decoupled.application.exceptions import (
    RequestExecutionError,
    TrainDatasetDataError,
    WorkspaceAlreadyExistsError,
    WorkspaceDoesNotExistsError,
)

from ..dependency_injection.dispatcher import Handler
from ..domain.models import (
    CategoryCollection,
    Workspace,
    WorkspaceId,
    WorkspaceName,
    WorkspaceOwnerId,
)
from .commands import (
    CreateOrUpdateWorkspaceFromUploadExcelFileCommand,
    CreateWorkspaceAndAddDataFromFileCommand,
    CreateWorkspaceCommand,
    TrainWorkspaceCommand,
    WorkspaceMetricsCommand,
)
from .dtos import (
    FileWorkspace,
    HTTPRequest,
    HTTPResponse,
    TrainDataSet,
    TrainingResponse,
    WorkspaceDTO,
)
from .interfaces import (
    IDataProcessor,
    IDomainSerializer,
    IExecutor,
    IFileProcessor,
    IFileReader,
    IFinder,
    IRepository,
)

logger = logging.getLogger(__name__)


# TODO: WIP
class CreateWorkspaceHandler(Handler):  # pylint: disable=too-few-public-methods
    """CreateWorkspace command handler."""

    _workspace_repository: IRepository[WorkspaceDTO]
    _workspace_finder: IFinder[WorkspaceDTO]
    _workspace_serializer: IDomainSerializer[Workspace, WorkspaceDTO]

    def __init__(
        self,
        workspace_repository: IRepository[WorkspaceDTO],
        workspace_finder: IFinder[WorkspaceDTO],
        workspace_serializer: IDomainSerializer[Workspace, WorkspaceDTO],
    ) -> None:
        """Class constructor."""
        self._workspace_repository = workspace_repository
        self._workspace_finder = workspace_finder
        self._workspace_serializer = workspace_serializer

    def handle(self, command: CreateWorkspaceCommand) -> None:
        """Handle the CreateWorkspaceCommand use case."""
        logger.info("Start Handling a '%s'", command)

        workspace = Workspace(
            id=WorkspaceId(value=self._workspace_repository.generate_uuid()),
            name=WorkspaceName(value=command.name),
            categories=CategoryCollection(),
            owner_id=WorkspaceOwnerId.from_string(value=command.owner_id),
        )

        self._workspace_repository.save(
            workspace=self._workspace_serializer.serialize(domain_obj=workspace)
        )

        logger.info("Command '%s' successfully executed.", command)


class TrainWorkspaceHandler(Handler):
    """TrainWorkspaceHandler class."""

    _data_processor: IDataProcessor[WorkspaceDTO, TrainDataSet]
    _workspace_repository: IRepository[WorkspaceDTO]
    _workspace_finder: IFinder[WorkspaceDTO]
    _requestor: IExecutor[HTTPRequest, HTTPResponse]
    _serializer: IDomainSerializer[Workspace, WorkspaceDTO]
    _flux_train_endpoint_url: str
    _flux_train_endpoint_method: str

    def __init__(
        self,
        data_processor: IDataProcessor[WorkspaceDTO, TrainDataSet],
        workspace_repository: IRepository[WorkspaceDTO],
        workspace_finder: IFinder[WorkspaceDTO],
        requestor: IExecutor[HTTPRequest, HTTPResponse],
        serializer: IDomainSerializer[Workspace, WorkspaceDTO],
        flux_train_endpoint_url: str,
        flux_train_endpoint_method: str,
    ) -> None:
        """Class constructior."""
        self._data_processor = data_processor
        self._workspace_repository = workspace_repository
        self._workspace_finder = workspace_finder
        self._requestor = requestor
        self._serializer = serializer
        self._flux_train_endpoint_url = flux_train_endpoint_url
        self._flux_train_endpoint_method = flux_train_endpoint_method

    def handle(self, command: TrainWorkspaceCommand) -> TrainingResponse:
        """Handle an TrainWorkspaceHandler."""
        response_obj: Dict[str, Any] = {
            "model_id": None,
            "success": True,
            "errors": None,
        }

        workspace_dto = self._workspace_finder.get(
            id=command.workspace_id, owner_id=command.owner
        )

        if workspace_dto is None:
            response_obj.update({"errors": "Object not found", "success": False})

            return TrainingResponse(**response_obj)

        try:
            train_dataset = self._data_processor.generate_dataset(
                workspaces=[workspace_dto]
            )

        except TrainDatasetDataError as error:
            response_obj.update({"errors": f"{error}", "success": False})

            return TrainingResponse(**response_obj)

        try:
            request = HTTPRequest(
                url=self._flux_train_endpoint_url,
                method=self._flux_train_endpoint_method,
                body=asdict(train_dataset),
                headers={"Host": "api.clasifica.io.localhost"},
            )
            http_response = self._requestor.execute(request=request)

        except Exception as error:
            response_obj.update({"errors": f"{error}", "success": False})

            return TrainingResponse(**response_obj)

        workspace = self._serializer.deserialize(dto=workspace_dto)

        workspace.set_model_id(model_id=http_response.body["model_id"])

        self._workspace_repository.update(
            workspace=self._serializer.serialize(domain_obj=workspace)
        )

        response_obj.update({"model_id": f"{http_response.body['model_id']}"})

        return TrainingResponse(**response_obj)


class CreateWorkspaceFromUploadExcelFileCommandHandler(
    Handler
):  # pylint: disable=too-few-public-methods
    """CreateWorkspaceFromUploadExcelFileCommandHandler command handler."""

    _workspace_repository: IRepository[WorkspaceDTO]
    _serializer: IDomainSerializer[Workspace, WorkspaceDTO]
    _file_reader: IFileReader[FileWorkspace]
    _workspace_finder: IFinder[WorkspaceDTO]
    _file_processor: IFileProcessor[Workspace, FileWorkspace, str]

    def __init__(
        self,
        workspace_repository: IRepository[WorkspaceDTO],
        serializer: IDomainSerializer[Workspace, WorkspaceDTO],
        file_reader: IFileReader[FileWorkspace],
        workspace_finder: IFinder[WorkspaceDTO],
        file_processor: IFileProcessor[Workspace, FileWorkspace, str],
    ) -> None:
        """Class constructor."""
        self._workspace_repository = workspace_repository
        self._file_reader = file_reader
        self._serializer = serializer
        self._workspace_finder = workspace_finder
        self._file_processor = file_processor

    def handle(
        self, command: CreateOrUpdateWorkspaceFromUploadExcelFileCommand
    ) -> None:
        """Handle an CreateOrUpdateWorkspaceFromUploadExcelFileCommand."""
        logger.info("Start Handling a '%s'", command)

        file_workspaces_set = self._file_reader.read_from_bytes(
            bytes=command.file_bytes
        )

        self._file_processor.process(
            file_workspaces=file_workspaces_set, owner=command.owner
        )

        for workspace in self._file_processor.new_objs:
            self._workspace_repository.save(
                workspace=self._serializer.serialize(domain_obj=workspace)
            )

        for workspace in self._file_processor.existing_objs:
            self._workspace_repository.update(
                workspace=self._serializer.serialize(domain_obj=workspace)
            )

        logger.info("Command '%s' successfully executed.", command)


class CreateWorkspaceAndAddDataFromFileCommandHandler(
    Handler[Optional[str]]
):  # pylint: disable=too-few-public-methods
    """CreateWorkspaceAndAddDataFromFileCommand Handler."""

    _workspace_repository: IRepository[WorkspaceDTO]
    _serializer: IDomainSerializer[Workspace, WorkspaceDTO]
    _file_reader: IFileReader[FileWorkspace]
    _file_processor: IFileProcessor[Workspace, FileWorkspace, str]

    def __init__(
        self,
        workspace_repository: IRepository[WorkspaceDTO],
        serializer: IDomainSerializer[Workspace, WorkspaceDTO],
        file_reader: IFileReader[FileWorkspace],
        file_processor: IFileProcessor[Workspace, FileWorkspace, str],
    ) -> None:
        """Class constructor."""
        self._workspace_repository = workspace_repository
        self._file_reader = file_reader
        self._serializer = serializer
        self._file_processor = file_processor

    def handle(
        self, command: CreateWorkspaceAndAddDataFromFileCommand
    ) -> Optional[str]:
        """Handle an AddDataToWorkspaceFromFileCommand."""
        logger.info("Start Handling a '%s'", command)

        file_workspaces_set = self._file_reader.read_from_bytes(
            bytes=command.file_bytes
        )

        file_workspace_names = [
            workspace_file.name for workspace_file in file_workspaces_set
        ]

        if command.workspace_name not in file_workspace_names:
            raise WorkspaceDoesNotExistsError(message=command.workspace_name)

        for workspace_file in file_workspaces_set:
            if command.workspace_name == workspace_file.name:
                self._file_processor.process(
                    file_workspaces={workspace_file}, owner=command.owner_id
                )

                if command.workspace_name in self._file_processor.existing_objs:
                    raise WorkspaceAlreadyExistsError(message=command.workspace_name)

                domain_worksapce = self._file_processor.get(name=command.workspace_name)

                assert domain_worksapce

                self._workspace_repository.save(
                    workspace=self._serializer.serialize(domain_obj=domain_worksapce)
                )

                return str(domain_worksapce.id.value)

        return None


class WorkspaceMetricsCommandHandler(Handler):
    """WorkspaceMetricsCommand Handler."""

    _data_processor: IDataProcessor[WorkspaceDTO, TrainDataSet]
    _workspace_repository: IRepository[WorkspaceDTO]
    _workspace_finder: IFinder[WorkspaceDTO]
    _requestor: IExecutor[HTTPRequest, HTTPResponse]
    _serializer: IDomainSerializer[Workspace, WorkspaceDTO]
    _flux_metrics_endpoint_url: str
    _flux_metrics_endpoint_method: str

    def __init__(
        self,
        data_processor: IDataProcessor[WorkspaceDTO, TrainDataSet],
        workspace_repository: IRepository[WorkspaceDTO],
        workspace_finder: IFinder[WorkspaceDTO],
        requestor: IExecutor[HTTPRequest, HTTPResponse],
        serializer: IDomainSerializer[Workspace, WorkspaceDTO],
        flux_metrics_endpoint_url: str,
        flux_metrics_endpoint_method: str,
    ) -> None:
        """Class constructior."""
        self._data_processor = data_processor
        self._workspace_repository = workspace_repository
        self._workspace_finder = workspace_finder
        self._requestor = requestor
        self._serializer = serializer
        self._flux_metrics_endpoint_url = flux_metrics_endpoint_url
        self._flux_metrics_endpoint_method = flux_metrics_endpoint_method

    def handle(self, command: WorkspaceMetricsCommand) -> Any:
        """Handle a WorkspaceMetricsCommand request."""
        workspace_dto = self._workspace_finder.get(
            id=command.workspace_id, owner_id=command.owner
        )

        if workspace_dto is None:
            raise WorkspaceDoesNotExistsError(message=command.workspace_id)

        dataset = self._data_processor.generate_dataset(workspaces=[workspace_dto])

        try:
            request = HTTPRequest(
                url=self._flux_metrics_endpoint_url,
                method=self._flux_metrics_endpoint_method,
                body=asdict(dataset),
                headers={"Host": "api.clasifica.io.localhost"},
            )
            http_response = self._requestor.execute(request=request)

        except Exception as error:
            raise RequestExecutionError(message=str(error)) from error

        workspace = self._serializer.deserialize(dto=workspace_dto)

        workspace.set_metrics(metrics=http_response.body["report"])

        self._workspace_repository.update(
            workspace=self._serializer.serialize(domain_obj=workspace)
        )


# TODO: WIP
# class CreateDocumentHandler(Handler):  # pylint: disable=too-few-public-methods
#     """Train command handler."""

#     _workspace_repository: Repository[Workspace]
#     _workspace_finder: Finder[Workspace]

#     def __init__(
#         self,
#         workspace_repository: Repository[Workspace],
#         workspace_finder: Finder[Workspace]
#     ) -> None:
#         """Class constructor."""
#         self._workspace_repository = workspace_repository
#         self._workspace_finder = workspace_finder

#     async def handle(self, command: CreateDocumentCommand) -> None:  # type: ignore
#         """Handle the creation of a document use case."""
#         logger.info("Start Handling '%s'", command)

#         workspace = self._workspace_finder.get_by_category_id(
#           category_id=CategoryId.from_string(value=command.category_id)
#         )

#         document = Document(
#             id=DocumentId.from_string(value=command.id),
#             text=DocumentText(command.text),
#             category_id=CategoryId.from_string(value=command.category_id)
#         )

#         workspace.add_document(document=document)

#         self._workspace_repository.save(obj=workspace)

#         logger.info("Command '%s' successfully executed.", command)
