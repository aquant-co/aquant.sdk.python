import datetime

from aquant.core.logger import Logger
from aquant.domains.security.entity import Security
from aquant.domains.security.utils import (
    decode_securities,
    encode_security,
    security_payload_builder,
)
from aquant.infra.nats import NatsClient


class SecurityService:
    def __init__(self, logger: Logger, nats_client: NatsClient) -> None:
        self.logger = logger
        self.nats_client = nats_client

    async def get_securities(
        self, ticker: str = None, asset: str = None, expires_at: datetime = None
    ) -> list[Security]:
        try:
            subject = "marketdata.security.request"
            payload = security_payload_builder(ticker, asset, expires_at)
            message = encode_security(payload=payload)
            response = await self.nats_client.request(subject, message, timeout=5)
            response_decoded = decode_securities(response=response)

            self.logger.info(f"Retrieved {len(response_decoded)} records.")

            return response_decoded
        except Exception as e:
            self.logger.error(
                f"Error trying to fetch securities for payload provided, payload {security_payload_builder(ticker, asset, expires_at)}, due: {e}"
            )
