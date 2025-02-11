import struct

import pandas as pd

from aquant.core.logger import Logger
from aquant.domains.broker.utils import parse_brokers_binary_to_string
from aquant.infra.nats import NatsClient


class BrokerService:
    def __init__(self, logger: Logger, nats_client: NatsClient) -> None:
        self.logger = logger
        self.nats_client = nats_client

    async def get_broker_by_fk_id(self, fk_id: int) -> pd.DataFrame:
        try:
            subject = "marketdata.broker.request"
            payload = struct.pack("!I", fk_id)
            response = await self.nats_client.request(subject, payload, timeout=2)
            return self._parse_brokers(response)
        except Exception as e:
            self.logger.error(
                f"Error trying to fetch brokers for fk_id provided. fk_id {fk_id}, due: {e}"
            )
            return pd.DataFrame()

    def _parse_brokers(self, data: bytes) -> pd.DataFrame:
        try:
            df = parse_brokers_binary_to_string(data)
            return df
        except Exception as e:
            self.logger.error(f"Error parsing brokers data: {e}")
            return pd.DataFrame()
