"""Container module."""
from typing import Dict, Type

from django_decoupled.application.services import (
    CategoryDomainSerializer,
    DocumentDomainSerializer,
    ExcelFileProcessor,
    WorkspaceDomainSerializer,
)
from django_decoupled.infrastructure.data_transformation.processors import (
    DataProcessorService,
)
from django_decoupled.infrastructure.requestor.executors import (
    HTTPExecutor,
    HTTPRequestValidator,
    HTTPResponseValidator,
)
from django.conf import settings

from ..application.commands import (
    CreateOrUpdateWorkspaceFromUploadExcelFileCommand,
    CreateWorkspaceAndAddDataFromFileCommand,
    CreateWorkspaceCommand,
    TrainWorkspaceCommand,
    WorkspaceMetricsCommand,
)
from ..application.handlers import (
    CreateWorkspaceAndAddDataFromFileCommandHandler,
    CreateWorkspaceFromUploadExcelFileCommandHandler,
    CreateWorkspaceHandler,
    TrainWorkspaceHandler,
    WorkspaceMetricsCommandHandler,
)
from ..controllers.services.file_readers import ExcelFileReader
from ..infrastructure.persistence.workspaces.finders import DjangoWorkspaceFinder
from ..infrastructure.persistence.workspaces.repositories import (
    DjangoWorkspaceRepository,
)
from ..infrastructure.persistence.workspaces.serializers import (
    CategoryDBSerializer,
    DocumentDBSerializer,
    WorkspaceDBSerializer,
)
from .dispatcher import Command, Dispatcher, Handler


class Container:
    """Container class."""

    config = settings
    document_db_serializer = DocumentDBSerializer()

    category_db_serializer = CategoryDBSerializer(
        document_serializer=document_db_serializer
    )
    workspace_db_serializer = WorkspaceDBSerializer(
        category_serializer=category_db_serializer
    )

    workspace_finder = DjangoWorkspaceFinder(
        workspace_serializer=workspace_db_serializer,
    )

    workspace_repository = DjangoWorkspaceRepository(
        workspace_finder=workspace_finder,
        workspace_serializer=workspace_db_serializer,
        category_serializer=category_db_serializer,
        document_serializer=document_db_serializer,
    )

    workspace_domain_serializer = WorkspaceDomainSerializer(
        category_serializer=CategoryDomainSerializer(
            document_serializer=DocumentDomainSerializer(),
        ),
    )

    file_processor = ExcelFileProcessor(
        workspace_finder=workspace_finder, serializer=workspace_domain_serializer
    )

    create_or_update_workspace_from_upload_excel_file_handler = (
        CreateWorkspaceFromUploadExcelFileCommandHandler(
            workspace_finder=workspace_finder,
            workspace_repository=workspace_repository,
            serializer=workspace_domain_serializer,
            file_reader=ExcelFileReader(),
            file_processor=file_processor,
        )
    )

    create_workspace_and_add_data_from_excel_handler = (
        CreateWorkspaceAndAddDataFromFileCommandHandler(
            workspace_repository=workspace_repository,
            serializer=workspace_domain_serializer,
            file_reader=ExcelFileReader(),
            file_processor=file_processor,
        )
    )

    create_workspace_handler = CreateWorkspaceHandler(
        workspace_repository=workspace_repository,
        workspace_finder=workspace_finder,
        workspace_serializer=workspace_domain_serializer,
    )

    requestor = HTTPExecutor(
        request_validator=HTTPRequestValidator(
            available_http_methods=config.REQUESTOR_AVAILABLE_HTTP_METHODS,
        ),
        response_validator=HTTPResponseValidator(),
    )

    train_workspace_handler = TrainWorkspaceHandler(
        data_processor=DataProcessorService(),
        workspace_repository=workspace_repository,
        workspace_finder=workspace_finder,
        requestor=requestor,
        serializer=workspace_domain_serializer,
        flux_train_endpoint_url=settings.FLUX_TRAIN_ENDPOINT_URL,
        flux_train_endpoint_method=settings.FLUX_TRAIN_ENDPOINT_METHOD,
    )

    workspace_metrics_command_handler = WorkspaceMetricsCommandHandler(
        data_processor=DataProcessorService(),
        workspace_repository=workspace_repository,
        workspace_finder=workspace_finder,
        requestor=requestor,
        serializer=workspace_domain_serializer,
        flux_metrics_endpoint_url=settings.FLUX_METRICS_ENDPOINT_URL,
        flux_metrics_endpoint_method=settings.FLUX_METRICS_ENDPOINT_METHOD,
    )

    handlers: Dict[Type[Command], Handler] = {
        CreateWorkspaceCommand: create_workspace_handler,
        CreateWorkspaceAndAddDataFromFileCommand: create_workspace_and_add_data_from_excel_handler,
        CreateOrUpdateWorkspaceFromUploadExcelFileCommand: create_or_update_workspace_from_upload_excel_file_handler,  # noqa: E501
        TrainWorkspaceCommand: train_workspace_handler,
        WorkspaceMetricsCommand: workspace_metrics_command_handler,
    }

    dispatcher: Dispatcher = Dispatcher(handlers=handlers)


container = Container()
