from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.dependencies.logger import create_logger
from app.core.logger.logger_interface import LoggerInterface


class LoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware for structured logging of incoming requests and outgoing responses.
    """

    def __init__(self, app, logger: LoggerInterface = None):
        super().__init__(app)
        self.logger = logger or create_logger(__name__)

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Middleware processing for logging and optional validations.
        """
        self.logger.info("LoggerMiddleware: Dispatch started")

        # Step 1: Log request metadata
        try:
            self.logger.info(
                {
                    "message": "Request metadata received",
                    "path": request.url.path,
                    "method": request.method,
                    "query_params": dict(request.query_params),
                    "headers": dict(request.headers),
                }
            )
        except Exception as e:
            self.logger.error(
                {"message": "Failed to log request metadata", "error": str(e)}
            )

        # Step 2: Log request body without modifying it
        try:
            # Reading the body safely without interfering
            body = await request.body()
            self.logger.info(
                {
                    "message": "Request body received",
                    "body": body.decode("utf-8"),
                }
            )
        except Exception as e:
            self.logger.error(
                {"message": "Failed to read request body", "error": str(e)}
            )

        # Step 3: Pass the request to the next handler
        try:
            self.logger.info("LoggerMiddleware: Processing request")
            response = await call_next(request)
            self.logger.info("LoggerMiddleware: Request processed successfully")
        except Exception as e:
            self.logger.error(
                {
                    "message": "Error processing request",
                    "path": request.url.path,
                    "method": request.method,
                    "error": str(e),
                }
            )
            raise e

        # Step 4: Log response metadata
        try:
            self.logger.info(
                {
                    "message": "Response details",
                    "path": request.url.path,
                    "method": request.method,
                    "status_code": response.status_code,
                }
            )
        except Exception as e:
            self.logger.error(
                {"message": "Failed to log response details", "error": str(e)}
            )

        self.logger.info("LoggerMiddleware: Dispatch completed")
        return response
