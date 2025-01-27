import pytest

from aquant_sdk.redis.processor import (
    LogMessageProcessor,
    MessageProcessor,
    PrintMessageProcessor,
)


def test_message_processor_not_implemented():
    processor = MessageProcessor()
    with pytest.raises(NotImplementedError):
        processor.process({"key": "value"})


def test_print_message_processor(capsys):
    processor = PrintMessageProcessor()
    message = {"key": "value"}
    processor.process(message)
    captured = capsys.readouterr()
    assert captured.out == f"Processed message: {message}\n"


def test_log_message_processor(capsys):
    processor = LogMessageProcessor()
    message = {"key": "value"}
    processor.process(message)
    captured = capsys.readouterr()
    assert captured.out == f"Log: {message}\n"
