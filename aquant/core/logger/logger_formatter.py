from pythonjsonlogger.json import JsonFormatter


class LoggerFormatter(JsonFormatter):
    """
    Custom JSON log formatter for structured logging.
    """

    def __init__(self):
        super().__init__(
            "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(lineno)d",
        )
