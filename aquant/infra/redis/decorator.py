from aquant.infra.redis.processor import MessageProcessor


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


class BufferedMessageProcessor(MessageProcessor):
    def __init__(self):
        self.buffer = []

    def process(self, data):
        self.buffer.append(data)
        if len(self.buffer) >= 1000:
            self.flush()

    def flush(self):
        self.buffer.clear()
