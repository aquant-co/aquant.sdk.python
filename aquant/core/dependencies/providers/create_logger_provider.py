from aquant.core.logger import Logger


def create_logger_provider(name: str) -> Logger:
    """
    Creates and returns a logger instance for dependency injection.

    Args:
        name(str): Logger name (module name).

    Returns:
        Logger: Configured logger instance.
    """
    return Logger(name)
