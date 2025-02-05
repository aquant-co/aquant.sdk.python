class MessageProcessor:
    def process(self, message: dict):
        raise NotImplementedError


class PrintMessageProcessor(MessageProcessor):
    def process(self, message: dict):
        pass


class LogMessageProcessor(MessageProcessor):
    def process(self, message):
        print(f"Log: {message}")


class BufferedMessageProcessor(MessageProcessor):
    def __init__(self):
        self.buffer = []

    def process(self, data):
        self.buffer.append(data)
        if len(self.buffer) >= 1000:
            self.flush()

    def flush(self):
        self.buffer.clear()
