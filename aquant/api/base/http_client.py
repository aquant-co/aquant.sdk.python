from typing import Any

from httpx import AsyncClient, HTTPStatusError, RequestError, TimeoutException

from aquant.api.base.http_exceptions import HTTPException
from aquant.api.base.interfaces import (
    HTTPClientInterface,
    HTTPExceptionInterface,
    LoggerInterface,
)
from aquant.api.base.types import RequestDataType


class HTTPClient(HTTPClientInterface):
    """
    HTTP Adapter for handling HTTP requests using HTTPX.
    """

    def __init__(
        self,
        logger: LoggerInterface,
        base_url: str = "",
        timeout: float | None = 10.0,
        exception_handler: HTTPExceptionInterface | None = None,
    ):
        """
        Initializes the HTTPAdapter.

        Args:
            base_url (str): Base URL for the HTTP client.
            timeout (float): Default timeout for requests.
            logger (LoggerInterface): Logger instance for structured logging.
            exception_handler (Optional[HTTPException]): Exception handler instance.
        """
        self.client = AsyncClient(base_url=base_url, timeout=timeout)
        self.logger = logger

        # Validação explícita
        self.exception_handler = exception_handler or HTTPException(logger)

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
        """
        Internal method to handle HTTP requests dynamically.
        """
        try:
            self.logger.debug(
                f"HTTP {
                    method.upper()} Request: URL={url}, Headers={headers}, Params={params}, Body={
                    json or data}"
            )

            response = await self.client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                timeout=timeout,
            )

            response.raise_for_status()

            self.logger.debug(
                f"HTTP {
                    method.upper()} Response: Status={
                    response.status_code}, Body={
                    response.text}"
            )

            return response

        except (HTTPStatusError, TimeoutException, RequestError) as err:
            self.logger.error(f"HTTP Error: {str(err)}")
            return self.exception_handler.handle_exception(err)

        except Exception as err:
            self.logger.error(f"Unexpected Error: {str(err)}")
            return self.exception_handler.handle_exception(err)

    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Executes an HTTP GET request."""
        return await self.request(
            "GET", url, headers=headers, params=params, timeout=timeout
        )

    async def post(
        self,
        url: str,
        data: RequestDataType | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Executes an HTTP POST request."""
        return await self.request(
            "POST", url, headers=headers, data=data, json=json, timeout=timeout
        )

    async def put(
        self,
        url: str,
        data: RequestDataType | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Executes an HTTP PUT request."""
        return await self.request(
            "PUT", url, headers=headers, data=data, json=json, timeout=timeout
        )

    async def patch(
        self,
        url: str,
        data: RequestDataType | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Executes an HTTP PATCH request."""
        return await self.request(
            "PATCH", url, headers=headers, data=data, json=json, timeout=timeout
        )

    async def delete(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Executes an HTTP DELETE request."""
        return await self.request("DELETE", url, headers=headers, timeout=timeout)

    async def close(self) -> None:
        """Closes the HTTP client session."""
        await self.client.aclose()
