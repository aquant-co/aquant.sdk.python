from nats.aio.client import Client as Nats
from nats.aio.errors import ErrNoServers, ErrTimeout

from aquant.core.logger import Logger
from aquant.infra.nats.nats_interface import NatsInterface


class NatsClient(NatsInterface):
    def __init__(
        self, logger: Logger, servers: list[str], user: str = None, password: str = None
    ) -> None:
        self.log = logger
        self.servers = servers
        self.user = user
        self.password = password
        self.nc = Nats()

    async def connect(self):
        """Connect to NATS."""
        try:
            await self.nc.connect(
                servers=self.servers, user=self.user, password=self.password
            )
            self.log.info("Connected to NATS servers.")
        except ErrNoServers as e:
            self.log.error(f"NATS servers not reachable: {e}")
            raise ErrNoServers from e

    async def subscribe(self, subject: str, callback):
        """Subscribe to a topic and define a callback for processing."""

        async def message_handler(msg):
            await callback(msg.subject, msg.data, msg.reply)

        try:
            await self.nc.subscribe(subject, cb=message_handler)
            self.log.info(f"Subscribed to topic: {subject}")
        except Exception as e:
            self.log.error(f"Cannot subscribe to NATS: {e}")
            raise Exception from e

    async def publish(self, subject: str, message):
        """Publish a message to a topic."""
        try:
            if isinstance(message, str):
                message = message.encode()
            await self.nc.publish(subject, message)
            self.log.info(f"Message published to {subject}")
        except Exception as e:
            self.log.error(f"Cannot publish to NATS: {e}")
            raise Exception from e

    async def request(self, subject: str, message, timeout: float = 2.0):
        """Send a request and wait for a response."""
        try:
            if isinstance(message, str):
                message = message.encode()
            response = await self.nc.request(subject, message, timeout=timeout)
            self.log.info(f"Request sent to {subject}, received response.")
            return response.data
        except ErrTimeout:
            self.log.error(f"Request to {subject} timed out.")
            return None
        except Exception as e:
            self.log.error(f"Error in request-response: {e}")
            raise Exception from e

    async def close(self):
        """Close the NATS connection."""
        await self.nc.close()
        self.log.info("NATS connection closed.")
