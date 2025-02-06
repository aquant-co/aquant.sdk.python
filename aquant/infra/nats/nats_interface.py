from abc import ABC, abstractmethod


class NatsInterface(ABC):
    """Abstracted interface for Nats communication"""

    @abstractmethod
    async def connect(self):
        raise NotImplementedError

    @abstractmethod
    async def subscribe(self, subject: str, callback):
        raise NotImplementedError

    @abstractmethod
    async def publish(self, subject: str, message: str):
        raise NotImplementedError

    @abstractmethod
    async def request(self, subject: str, message: str, timeout: float = 2.0):
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        raise NotImplementedError
