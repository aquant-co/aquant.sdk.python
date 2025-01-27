from abc import ABC, abstractmethod
from typing import Any

from .types import RequestDataType


class HTTPClientInterface(ABC):
    """
    Interface for HTTP Adapter, ensuring compatibility with HTTPX.
    """

    @abstractmethod
    async def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: RequestDataType | None = None,
        json: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Sends an HTTP request."""

    @abstractmethod
    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Performs an HTTP GET request."""

    @abstractmethod
    async def post(
        self,
        url: str,
        data: RequestDataType | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Performs an HTTP POST request."""

    @abstractmethod
    async def put(
        self,
        url: str,
        data: RequestDataType | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Performs an HTTP PUT request."""

    @abstractmethod
    async def patch(
        self,
        url: str,
        data: RequestDataType | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Performs an HTTP PATCH request."""

    @abstractmethod
    async def delete(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Performs an HTTP DELETE request."""

    @abstractmethod
    async def close(self) -> None:
        """Closes the HTTP client session."""
