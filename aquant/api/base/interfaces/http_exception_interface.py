from abc import ABC, abstractmethod
from typing import Any

from httpx import HTTPStatusError, RequestError, TimeoutException


class HTTPExceptionInterface(ABC):
    """
    Interface for handling HTTP exceptions.
    """

    @abstractmethod
    def handle_http_error(self, error: HTTPStatusError) -> dict[str, Any]:
        """Handles HTTP status errors."""

    @abstractmethod
    def handle_request_error(self, error: RequestError) -> dict[str, Any]:
        """Handles request errors."""

    @abstractmethod
    def handle_timeout_error(self, error: TimeoutException) -> dict[str, Any]:
        """Handles timeout errors."""

    @abstractmethod
    def handle_exception(self, error: Exception) -> dict[str, Any]:
        """Handles generic exceptions."""
