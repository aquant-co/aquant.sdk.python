from typing import Optional

from app.core.logger.logger import LoggerInterface
from app.core.dependencies.logger import create_logger

class AppError(Exception):
    """Base Class for custom exceptions from application.

    Args:
        message (str): Error message
        details (Optional[str]): Aditional details for the error.
    """
    def __init__(
            self, 
            message: str, 
            details: Optional[str] = None,
            logger: Optional[LoggerInterface] = None
            ) -> None:
        super().__init__(message)
        self.message = message
        self.details = details
        self.logger = logger or create_logger(__name__)

        self.logger.error(self.__str__())

    def __str__(self):
        return f"{self.message} - Details: {self.details}" if self.details else self.message
