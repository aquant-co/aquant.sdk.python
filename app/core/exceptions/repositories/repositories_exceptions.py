from typing import Optional
from app.core.exceptions.app import AppError
from app.core.logger.logger import LoggerInterface

class RepositoryError(AppError):
    """Exception for repository layer errors."""
    def __init__(self, message: str, details: Optional[str] = None, logger: Optional[LoggerInterface] = None):
        super().__init__(message, details, logger)
