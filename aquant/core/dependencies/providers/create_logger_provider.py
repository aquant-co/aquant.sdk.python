import logging
import sys

from aquant.core.logger import Logger, LoggerFormatter


def create_logger_provider(name: str) -> Logger:
    """
    Creates and returns a logger instance for dependency injection.

    Args:
        name(str): Logger name (module name).

    Returns:
        Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        formatter = LoggerFormatter()
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
    return logger
