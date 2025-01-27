from aquant_sdk.redis.processor import MessageProcessor


class LoggingProcessor(MessageProcessor):
    def __init__(self, processor: MessageProcessor) -> None:
        self._processor = processor

    def process(self, message: dict):
        self._processor.process(message)


class MessageProcessor(MessageProcessor):
    def __init__(self, processor: MessageProcessor) -> None:
        self._processor = processor

    def process(self, message: dict):
        self._processor.process(message)
