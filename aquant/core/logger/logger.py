import logging
import sys

from aquant.core.logger.logger_formatter import LoggerFormatter
from aquant.core.logger.logger_interface import LoggerInterface


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
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        # Formatter for structured logs
        formatter = LoggerFormatter()

        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        # Avoid duplicate handlers
        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)

    def info(self, message: str) -> None:
        """
        Logs an info message.

        Args:
            message (str): Log message.
        """
        self.logger.info(message)

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
