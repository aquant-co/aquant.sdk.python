import struct
from datetime import datetime

import pandas as pd

from aquant.core.logger import Logger
from aquant.domains.trade.utils import parse_trades_binary_to_dataframe
from aquant.infra.nats import NatsClient


class TradeService:
    def __init__(self, logger: Logger, nats_client: NatsClient) -> None:
        self.logger = logger
        self.nats_client = nats_client

    async def get_trades(
        self, start_time: datetime, end_time: datetime
    ) -> pd.DataFrame:
        try:
            subject = "marketdata.request"
            payload = struct.pack("!dd", start_time.timestamp(), end_time.timestamp())
            response = await self.nats_client.request(subject, payload, timeout=2)
            return self._parse_trades(response)
        except Exception as e:
            self.logger.error(
                f"Error trying to fetch trades for timerange provided. start_time: {start_time}, end_time: {end_time}, due: {e}"
            )
            return pd.DataFrame()

    def _parse_trades(self, data: bytes) -> pd.DataFrame:
        try:
            df = parse_trades_binary_to_dataframe(data)
            return df
        except Exception as e:
            self.logger.error(f"Error parsing trades data: {e}")
            return pd.DataFrame()
