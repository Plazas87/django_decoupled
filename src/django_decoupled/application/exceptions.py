"""Exception module."""


class DataError(Exception):
    """Base Expection for Data errors."""


class RequestException(Exception):
    """Base Expection for Requests."""


class PersistenceError(Exception):
    """Base class for Persistence exceptions."""


class WorkspaceDoesNotExistsError(PersistenceError):
    """Raised when trying to save a Workspace that already exists."""

    def __init__(self, message: str) -> None:
        """Class constructor."""
        self.message = f"The Workspace '{message}' does not exist in the database."
        super().__init__(self.message)


class WorkspaceAlreadyExistsError(PersistenceError):
    """Raised when trying to update a Workspace that does not already exist."""

    def __init__(self, message: str) -> None:
        """Class constructor."""
        self.message = f"The Workspace '{message}' already exists in teh database."
        super().__init__(self.message)


class ResponseError(Exception):
    """Base Expection for Responses."""

    def __init__(self, status_code: int, body: str) -> None:
        """Class constructor."""  # noqa: D401
        self.body = body
        self.status_code = status_code
        super().__init__(self.body)

    def __str__(self) -> str:
        """Nice string representation."""
        return (
            f"{self.__class__.__name__}(status_code={self.status_code}, body={self.body})"
        )

    def __repr__(self) -> str:
        """Nice string representation."""
        return (
            f"{self.__class__.__name__}(status_code={self.status_code}, body={self.body})"
        )


class InvalidURLRequestorException(RequestException):
    """
    Exception raised when the url is not a valid one.

    Attributes
        url(str) -- the url.
    """

    def __init__(self, url: str) -> None:
        """Class constructor."""  # noqa: D401
        self.message = f"Invalid URL: '{url}'."
        super().__init__(self.message)


class InvalidHeadersRequestorException(RequestException):
    """Exception raised when the headers are not valid."""

    def __init__(self, message: str) -> None:
        """Class constructor."""  # noqa: D401
        self.message = f"Invalid Headers exception '{message}'."
        super().__init__(self.message)


class RequestBuildException(RequestException):
    """Exception raised when the headers are not valid."""

    def __init__(self, message: str) -> None:
        """Class constructor."""  # noqa: D401
        self.message = f"RequestBuildingException: {message}"
        super().__init__(self.message)


class RequestExecutionError(RequestException):
    """Exception raised when the Resquest cannot be executed."""

    def __init__(self, message: str) -> None:
        """Class constructor."""  # noqa: D401
        self.message = f"RequestExecutionError: {message}"
        super().__init__(self.message)


class InvalidHTTPMetodException(RequestException):
    """Exception raised when the Resquest has an invalid method."""

    def __init__(self, message: str) -> None:
        """Class constructor."""  # noqa: D401
        self.message = f"InvalidHTTPMetodException. Available methods {message}"
        super().__init__(self.message)


class HTTP403ForbiddenError(ResponseError):
    """Exception raised when the Response contain a 403 status code."""


class HTTP404NotFoundError(ResponseError):
    """Exception raised when the Response contain a 404 status code."""


class HTTP500InternalServerError(ResponseError):
    """Exception raised when the Response contain a 500 status code."""


class HTTP503ServiceUnavailableError(ResponseError):
    """Exception raised when the Response contain a 503 status code."""


class UnhandledHttpStatusCodeError(ResponseError):
    """Exception raised when the Response contain an unhandled status code."""


class TrainDatasetDataError(DataError):
    """Exception raised when there is an error while generating the TRain Dataset."""
