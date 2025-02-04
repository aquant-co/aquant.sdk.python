from typing import Any

from httpx import HTTPStatusError, RequestError, TimeoutException

from aquant.api.base.interfaces import HTTPExceptionInterface, LoggerInterface


class HTTPException(HTTPExceptionInterface):
    """
    Concrete implementation for HTTPExceptionInterface.
    """

    def __init__(self, logger: LoggerInterface):
        """
        Initializes the handler with a logger.

        Args:
            logger (LoggerInterface): Logger instance for recording errors.
        """
        self.logger = logger

    def handle_http_error(self, error: HTTPStatusError) -> dict[str, Any]:
        """Handles HTTP status errors."""
        self.logger.error(
            f"HTTP Error: {error.response.status_code} - {error.response.text}"
        )
        return {
            "error": f"HTTP Error: {error.response.status_code} - {error.response.text}"
        }

    def handle_request_error(self, error: RequestError) -> dict[str, Any]:
        """Handles request errors."""
        self.logger.error(f"Request Error: {str(error)}")
        return {"error": f"Request Error: {str(error)}"}

    def handle_timeout_error(self, error: TimeoutException) -> dict[str, Any]:
        """Handles timeout errors."""
        self.logger.error("Request timed out.")
        return {"error": "Request timed out. Please try again later."}

    def handle_exception(self, error: Exception) -> dict[str, Any]:
        """Handles unexpected errors."""
        self.logger.error(f"Unexpected Error: {str(error)}")
        return {"error": f"Unexpected Error: {str(error)}"}
