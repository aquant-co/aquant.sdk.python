from abc import ABC, abstractmethod


class LoggerInterface(ABC):
    """
    Abstract interface for a logger implementation.

    Methods:
        info(message): Logs an informational message.
        error(message): Logs an error message.
        warning(message): Logs a warning message.
        debug(message): Logs a debug message.
    """

    @abstractmethod
    def info(self, message: str) -> None:
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        pass

    @abstractmethod
    def debug(self, message: str) -> None:
        pass
