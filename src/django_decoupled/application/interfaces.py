"""Application services module."""
from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, Set, TypeVar
from uuid import UUID

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


class IRepository(ABC, Generic[V]):
    """Interface for the repositories."""

    @staticmethod
    @abstractmethod
    def generate_uuid() -> UUID:
        """Generate an uuid."""

    @abstractmethod
    def save(self, workspace: V) -> None:
        """Save an obj in the database."""

    @abstractmethod
    def update(self, workspace: V) -> None:
        """Update an obj in the database."""


class IFinder(ABC, Generic[V]):
    """Interface for finders."""

    @abstractmethod
    def get(self, id: str, owner_id: str) -> V:
        """Get all available worksapaces by ID."""

    @abstractmethod
    def get_by_name(self, name: str, owner_id: str) -> V:
        """Get all available worksapaces by name and owner ID."""

    @abstractmethod
    def get_all(self, owner_id: str) -> List[V]:
        """Get all available worksapaces by owner ID."""

    @abstractmethod
    def exists(self, name: str, owner_id: str) -> bool:
        """Check if the instance exists in the database."""


class IDomainSerializer(ABC, Generic[V, K]):
    """IDomainSerializer Interface."""

    @abstractmethod
    def serialize(self, domain_obj: V) -> K:
        """
        Serialize a Domain instance into a DTO instance .

        Args:
            workspace (V): Domain instance

        Returns
            K: DTO instance
        """

    @abstractmethod
    def deserialize(self, dto: K) -> V:
        """
        Deserialize a DTO instance to Domain instance.

        Args:
            domain_obj (K): DTO isntance

        Returns
            V: Domain instance.
        """


class IDBSerializer(ABC, Generic[K, V]):
    """Serializer interface."""

    @abstractmethod
    def serialize(self, database_obj: K) -> V:
        """
        Serialize a Database instance to a DTO instance.

        Args:
            database_obj (K): database instance

        Returns
            V: DTO instance.
        """

    @abstractmethod
    def deserialize(self, dto: V) -> K:
        """
        Deserialize a DTO instance into a Database instance.

        Args:
            dto (K): database instance

        Returns
            V: database instance.
        """


class IFileReader(ABC, Generic[K]):
    """IFileReader interface."""

    @abstractmethod
    def read_from_bytes(self, bytes: bytes) -> Set[K]:
        """Read file from bytes."""
        ...


class IValidator(ABC):
    """Validator interface."""

    @staticmethod
    @abstractmethod
    def validate(value: Any) -> None:
        """Validate the value parameter."""


class IFileProcessor(ABC, Generic[K, V, T]):
    """FileProcessor interface."""

    @property
    @abstractmethod
    def new_objs(self) -> Set[K]:
        """Return new instances found within the File."""

    @property
    @abstractmethod
    def existing_objs(self) -> Set[K]:
        """Return existing instances found within the File."""

    @abstractmethod
    def process(self, file_workspaces: Set[V], owner: T) -> None:
        """Process intances within a file."""

    def get(self, name: T) -> Optional[K]:
        """Return an file instance by name."""


class IRequestValidator(ABC, Generic[K]):  # pylint: disable=R0903
    """RequestValidator Abstract base class."""

    @abstractmethod
    def validate(self, obj: K) -> None:
        """
        Validate a request.

        Args:
            obj (Request): Resquest to validate.

        """


class IResponseValidator(ABC, Generic[K]):  # pylint: disable=R0903
    """ResponseValidator Abstract base class."""

    @abstractmethod
    def validate(self, obj: K) -> None:
        """
        Validate a response.

        Args:
            obj (Response): Response to validate.

        """


class IExecutor(ABC, Generic[K, V]):  # pylint: disable=too-few-public-methods
    """Executor Abstrac class."""

    @abstractmethod
    def execute(self, request: K) -> V:
        """
        Execute a request.

        Args:
            request (Request): contains the information to perform the request

        Returns
            Response: request response
        """


class IDataProcessor(ABC, Generic[K, V]):
    """IDataProcessor interface."""

    @abstractmethod
    def generate_dataset(self, workspaces: List[K]) -> V:
        """Create the Train dataset based on data."""
