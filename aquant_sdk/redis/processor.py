class MessageProcessor:
    def process(self, message: dict):
        raise NotImplementedError


class PrintMessageProcessor(MessageProcessor):
    def process(self, message: dict):
        print(f"Processed message: {message}")


class LogMessageProcessor(MessageProcessor):
    def process(self, message):
        print(f"Log: {message}")
