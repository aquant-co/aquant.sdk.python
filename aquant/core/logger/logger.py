import logging
import sys

from aquant.core.logger.logger_formatter import LoggerFormatter
from aquant.core.logger.logger_interface import LoggerInterface
from aquant.settings import settings


class Logger(LoggerInterface):
    """
    Logger implementation using JSON formatting.
    """

    def __init__(self, name: str):
        """
        Initializes a JSON logger.

        Args:
            name (str): Logger name, typically the module name.
        """

        raw = settings.LOG_LEVEL
        if isinstance(raw, str):
            level = getattr(logging, raw.upper(), logging.INFO)
        elif isinstance(raw, int):
            level = raw
        else:
            level = logging.INFO

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False
        self.logger.handlers.clear()

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(LoggerFormatter())
        self.logger.addHandler(handler)

    def info(self, message: str) -> None:
        """
        Logs an info message.

        Args:
            message (str): Log message.
        """
        self.logger.debug(message)

    def error(self, message: str) -> None:
        """
        Logs an error message.

        Args:
            message (str): Log message.
        """
        self.logger.error(message)

    def warning(self, message: str) -> None:
        """
        Logs a warning message.

        Args:
            message (str): Log message.
        """
        self.logger.warning(message)

    def debug(self, message: str) -> None:
        """
        Logs a debug message.

        Args:
            message (str): Log message.
        """
        self.logger.debug(message)
