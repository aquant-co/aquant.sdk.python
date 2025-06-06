from datetime import datetime

import pandas as pd

from aquant.core.logger import Logger
from aquant.domains.trade.codecs import TradeParserService, TradePayloadBuilderService
from aquant.domains.trade.entity import OpenHighLowCloseVolume
from aquant.domains.trade.utils.enums import TimescaleIntervalEnum
from aquant.infra.nats import NatsClient, NatsSubjects


class TradeService:
    def __init__(
        self,
        logger: Logger,
        nats_client: NatsClient,
        trade_payload_builder_service: TradePayloadBuilderService,
        trade_parser_service: TradeParserService,
    ) -> None:
        self.logger = logger
        self.nats_client = nats_client
        self.trade_payload_builder_service = trade_payload_builder_service
        self.trade_parser_service = trade_parser_service

    async def get_trades(
        self,
        ticker: str | None = None,
        interval: TimescaleIntervalEnum | None = None,
        asset: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        ohlcv: bool | None = False,
    ) -> pd.DataFrame | OpenHighLowCloseVolume:
        try:
            subject = NatsSubjects.MARKETDATA_TRADE_REQUEST.value
            payload = self.trade_payload_builder_service.trade_payload_builder(
                ticker=ticker,
                interval=interval,
                asset=asset,
                start_time=start_time,
                end_time=end_time,
                ohlcv=ohlcv,
            )
            message = self.trade_parser_service.encode(message=payload)
            response = await self.nats_client.request(subject, message, timeout=20)

            if not ohlcv:
                return self.trade_parser_service.decode_trades_into_dataframe(response)

            return self.trade_parser_service.decode_ohlcv_into_dataframe(response)

        except Exception as e:
            params = {
                "ticker": ticker,
                "interval": interval,
                "asset": asset,
                "start_time": start_time,
                "end_time": end_time,
            }
            self.logger.error(
                f"Error trying to fetch trades or open high low close volume with the parameters provided: {params}, due: {e}"
            )
            raise e
