import asyncio

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
        self.reconnect_attempts = 3

    async def connect(self):
        """Tenta conectar ao NATS com reconexão automática."""
        for attempt in range(self.reconnect_attempts):
            try:
                await self.nc.connect(
                    servers=self.servers, user=self.user, password=self.password
                )
                self.log.info(f"Connected to NATS servers on attempt {attempt + 1}.")
                return
            except ErrNoServers as e:
                self.log.error(
                    f"NATS servers not reachable on attempt {attempt + 1}: {e}"
                )
                if attempt < self.reconnect_attempts - 1:
                    await asyncio.sleep(2)
                else:
                    raise ErrNoServers from e

    async def subscribe(self, subject: str, callback):
        """Inscreve-se em um tópico e define um callback para processar mensagens."""

        async def message_handler(msg):
            await callback(msg.subject, msg.data, msg.reply)

        try:
            await self.nc.subscribe(subject, cb=message_handler)
            self.log.info(f"Subscribed to topic: {subject}")
        except Exception as e:
            self.log.error(f"Cannot subscribe to NATS: {e}")
            raise Exception from e

    async def publish(self, subject: str, message):
        """Publica uma mensagem em um tópico do NATS."""
        try:
            if isinstance(message, str):
                message = message.encode()
            await self.nc.publish(subject, message)
            self.log.info(f"📤 Message published to {subject}")
        except Exception as e:
            self.log.error(f"❌ Cannot publish to NATS: {e}")
            raise Exception from e

    async def request(self, subject: str, message, timeout: float = 2.0):
        """Envia uma requisição e aguarda uma resposta."""
        try:
            if isinstance(message, str):
                message = message.encode()

            response = await self.nc.request(subject, message, timeout=timeout)

            return response.data

        except ErrTimeout:
            self.log.error(f"Request to {subject} timed out.")
            return None
        except Exception as e:
            self.log.error(f"Error in request-response: {e}")
            raise Exception from e

    async def close(self):
        """Fecha a conexão com o NATS."""
        await self.nc.close()
        self.log.info("🔌 NATS connection closed.")
