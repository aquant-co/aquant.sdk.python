from typing import Any

from httpx import ConnectTimeout, HTTPStatusError, ReadTimeout, RequestError

from app.core.logger.logger_interface import LoggerInterface

from .http_exception_handler_interface import HTTPExceptionHandlerInterface


class HTTPExceptionHandler(HTTPExceptionHandlerInterface):
    """
    Exception handler implementation using Object Literal Pattern.
    """

    def __init__(self, logger: LoggerInterface):
        """
        Initializes the handler with a logger.

        Args:
            logger (LoggerInterface): Logger instance for logging errors.
        """
        self.logger = logger

        self.handlers: dict[type[Exception], Any] = {
            RequestError: self.handle_request_error,
            HTTPStatusError: self.handle_http_error,
            ConnectTimeout: self.handle_timeout_error,
            ReadTimeout: self.handle_timeout_error,
            Exception: self.handle_generic_error,  # Default fallback
        }

    def handle_http_error(self, error: Exception) -> dict[str, Any]:
        """
        Handles HTTP status errors.

        Args:
            error (Exception): HTTP-related errors.

        Returns:
            dict[str, Any]: Formatted response with details.
        """
        self.logger.error(f"HTTP Error: {str(error)}")

        if isinstance(error, HTTPStatusError):
            return {
                "error": "HTTP error occurred.",
                "status_code": error.response.status_code,
                "message": str(error),
            }

        return self.handle_generic_error(error)

    def handle_request_error(self, error: Exception) -> dict[str, Any]:
        """
        Handles request errors.

        Args:
            error (Exception): Request-related errors.

        Returns:
            dict[str, Any]: Formatted response with details.
        """
        self.logger.error(f"Request Error: {str(error)}")

        # Verifica se o erro é do tipo RequestError
        if isinstance(error, RequestError):
            return {
                "error": "Request error occurred.",
                "details": str(error),
            }

        return self.handle_generic_error(error)

    def handle_exception(self, error: Exception) -> dict[str, Any]:
        """
        Handles generic exceptions dynamically based on registered handlers.

        Args:
            error (Exception): Exception to be handled.

        Returns:
            dict[str, Any]: Response containing the error details.
        """
        # Verifica se existe um handler registrado para o tipo de erro
        handler = self.handlers.get(type(error), self.handle_generic_error)
        return handler(error)

    def handle_timeout_error(self, error: Exception) -> dict[str, Any]:
        self.logger.error(f"Timeout Error: {str(error)}")
        return {
            "error": "Request timed out.",
            "details": str(error),
        }

    def handle_generic_error(self, error: Exception) -> dict[str, Any]:
        self.logger.error(f"Unexpected Error: {str(error)}")
        return {
            "error": "An unexpected error occurred.",
            "details": str(error),
        }
