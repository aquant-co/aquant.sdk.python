from app.core.dependencies.logger import create_logger
from app.core.exceptions.http import HTTPExceptionHandler
from app.core.logger import LoggerInterface


def create_logger_instance() -> LoggerInterface:
    """
    Factory function for creating a logger instance.

    Returns:
        LoggerInterface: An instance of a logger.
    """
    return create_logger("http_exception_handler")


def get_http_exception_handler(
    logger: LoggerInterface = None,
) -> HTTPExceptionHandler:
    """
    Dependency Injection for HTTPExceptionHandler.

    Args:
        logger (LoggerInterface): Logger instance for error logging.

    Returns:
        HTTPExceptionHandler: Instance of HTTPExceptionHandler.
    """
    if logger is None:  # Resolve logger if not provided
        logger = create_logger_instance()
    return HTTPExceptionHandler(logger)
