import logging
import sys

from app.core.logger import JsonLogFormatter, LoggerInterface


def create_logger(name: str) -> LoggerInterface:
    """
    Creates and returns a logger instance for dependency injection.

    Args:
        name(str): Logger name (module name).

    Returns:
        LoggerInterface: Configured logger instance.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        formatter = JsonLogFormatter()

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
