from app.core.exceptions.http import HTTPExceptionHandler
from app.core.logger.logger import Logger
from app.infra.adapters.http import HTTPAdapter


def get_http_adapter() -> HTTPAdapter:
    """
    Creates and returns an instance of HTTPAdapter.

    Returns:
        HTTPAdapter: Configured HTTP adapter instance.
    """
    logger = Logger(name="http_adapter")
    exception_handler = HTTPExceptionHandler(logger)
    return HTTPAdapter(logger=logger, exception_handler=exception_handler)
