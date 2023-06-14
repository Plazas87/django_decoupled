"""Executors module."""
# pylint: disable=all
import logging
from typing import Dict, List, Optional, Type, Union

import httpx
from django_decoupled.application.dtos import HTTPRequest, HTTPResponse

from ...application.exceptions import (
    HTTP403ForbiddenError,
    HTTP404NotFoundError,
    HTTP500InternalServerError,
    HTTP503ServiceUnavailableError,
    InvalidHeadersRequestorException,
    InvalidHTTPMetodException,
    InvalidURLRequestorException,
    RequestExecutionError,
    UnhandledHttpStatusCodeError,
)
from ...application.interfaces import IExecutor, IRequestValidator, IResponseValidator

logger = logging.getLogger(__name__)


StatusCodeErrorClassMap = Dict[
    int,
    Type[
        Union[
            HTTP403ForbiddenError,
            HTTP404NotFoundError,
            HTTP500InternalServerError,
            HTTP503ServiceUnavailableError,
            UnhandledHttpStatusCodeError,
        ]
    ],
]


class HTTPRequestValidator(IRequestValidator[HTTPRequest]):
    """HTTPRequestValidator class."""

    _available_http_methods: List[str]

    def __init__(self, available_http_methods: List[str]) -> None:
        """Class constructor."""
        self._available_http_methods = available_http_methods

    def validate(self, obj: HTTPRequest) -> None:
        """
        Validate a HTTP request.

        Args:
            obj (HTTPRequest): Resquest to validate.

        """
        self._process_request(obj=obj)

    def _process_request(self, obj: HTTPRequest) -> None:
        logger.debug("Start request validation process...")

        try:
            self._validate_url(url=obj.url)
        except Exception:
            raise InvalidURLRequestorException(url=obj.url)

        # Create the Headers
        try:
            self._validate_headers(headers=obj.headers)
        except Exception as error:
            raise InvalidHeadersRequestorException(str(error))

        try:
            self._validate_http_method(method=obj.method)
        except Exception:
            raise InvalidHTTPMetodException(str(self._available_http_methods))

        logger.debug(
            "Request validation completed. URL: '%s' - body: '%s'",
            obj.url,
            str(obj.body),
        )

    def _validate_url(self, url: str) -> None:
        allowed_schemes = ["http", "https"]
        httx_url = httpx.URL(url)

        assert httx_url.scheme in allowed_schemes

    def _validate_headers(self, headers: Optional[Dict[str, str]]) -> None:
        httpx.Headers(headers)

    def _validate_http_method(self, method: str) -> None:
        assert method in self._available_http_methods


class HTTPResponseValidator(IResponseValidator[httpx.Response]):
    """HTTPResponseValidator class."""

    _status_code_error_class_map: StatusCodeErrorClassMap

    def __init__(self) -> None:
        """Class constructor."""
        self._status_code_error_class_map: StatusCodeErrorClassMap = {
            403: HTTP403ForbiddenError,
            404: HTTP404NotFoundError,
            500: HTTP500InternalServerError,
            503: HTTP503ServiceUnavailableError,
        }

    def validate(self, obj: httpx.Response) -> None:
        """
        Validate a HTTP response.

        Args:
            obj (HTTPResponse): Response to validate.

        """
        self._process_status_code(obj=obj)

    def _process_status_code(self, obj: httpx.Response) -> None:
        """
        Validadate the response by its status code.

        If the response's status code is diferent from 200 raise and Exception,
        returns None otherwise.

        Args:
            obj (httpx.Response): Http response.

        Raises
            UnhandledHttpStatusCodeError: Raised when the response status code is unknown
            HTTP403ForbiddenError: Raised when the response status is 403
            HTTP404NotFoundError: Raised when the response status is 404
            HTTP500InternalServerError: Raised when the response status is 500
            HTTP503ServiceUnavailableError: Raised when the response status is 503
        """
        if obj.status_code == httpx.codes.OK:
            return None

        try:
            error_message = obj.json()
        except httpx.HTTPError as err:
            error_message = f"HTTP Exception for {err.request.url} - {err}"

        try:
            status_code_error_class = self._status_code_error_class_map[obj.status_code]

        except KeyError:
            status_code_error_class = UnhandledHttpStatusCodeError

        raise status_code_error_class(
            status_code=obj.status_code, body=str(error_message)
        )


class HTTPExecutor(
    IExecutor[HTTPRequest, HTTPResponse]
):  # pylint: disable=too-few-public-methods
    """HTTP Executor."""

    _request_validator: IRequestValidator[HTTPRequest]
    _response_validator: IResponseValidator[httpx.Response]

    def __init__(
        self,
        request_validator: IRequestValidator[HTTPRequest],
        response_validator: IResponseValidator[httpx.Response],
    ) -> None:
        """Class Constructor."""
        self._request_validator = request_validator
        self._response_validator = response_validator

    def execute(self, request: HTTPRequest) -> HTTPResponse:
        """
        Execute a request.

        Args:
            request (HTTPRequest): contains the information to perform the request

        Returns
            HTTPResponse: HTTP request response
        """
        logger.info(
            "Start executing a request to '%s' with payload '%s'",
            request.url,
            request.body,
        )
        logger.debug("Request: '%s'", request)

        # Validate the Request
        self._request_validator.validate(obj=request)

        http_request = self._build_request(request=request)
        try:
            with httpx.Client() as client:
                response = client.send(http_request)

        except Exception as error:
            logger.error(
                "Request execution ERROR: '%s' -- PAYLOAD: '%s' -- URL: '%s'",
                str(error),
                request.body,
                request.url,
            )
            raise RequestExecutionError(str(error))

        # Validate the Response
        self._response_validator.validate(obj=response)

        http_response = HTTPResponse(
            status_code=response.status_code,
            headers=dict(response.headers.items()),
            body=response.json(),
        )

        logger.debug(
            "Request execution RESPONSE: '%s' -- PAYLOAD: '%s' -- URL: '%s'",
            str(http_response.body),
            request.body,
            request.url,
        )

        logger.info(
            "Request execution to '%s' with payload '%s' sucessfully completed.",
            request.url,
            request.body,
        )

        return http_response

    # def execute(self, request: HTTPRequest) -> HTTPResponse:
    #     """
    #     Execute a request.

    #     Args:
    #         request (HTTPRequest): contains the information to perform the request

    #     Returns
    #         HTTPResponse: HTTP request response
    #     """
    #     logger.info(
    #         "Start executing a request to '%s' with payload '%s'",
    #         request.url,
    #         request.body,
    #     )
    #     logger.debug("Request: '%s'", request)

    #     http_response = HTTPResponse(
    #         status_code=200,
    #         headers={},
    #         body={"model_id": "fake_model_id", "metrics": {}},
    #     )

    #     logger.debug(
    #         "Request execution RESPONSE: '%s' -- PAYLOAD: '%s' -- URL: '%s'",
    #         str(http_response.body),
    #         request.body,
    #         request.url,
    #     )

    #     logger.info(
    #         "Request execution to '%s' with payload '%s' sucessfully completed.",
    #         request.url,
    #         request.body,
    #     )

    #     return http_response

    def _build_request(self, request: HTTPRequest) -> httpx.Request:
        headers = {"Content-Type": "application/json"}

        if request.headers:
            headers = {**headers, **request.headers}

        return httpx.Request(
            method=request.method,
            url=request.url,
            json=request.body,
            headers=headers,
        )
