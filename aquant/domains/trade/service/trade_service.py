from datetime import datetime

import pandas as pd

from aquant.core.logger import Logger
from aquant.domains.trade.entity import OpenHighLowCloseVolume
from aquant.domains.trade.service.trade_parser_service import TradeParserService
from aquant.domains.trade.service.trade_payload_builder_service import (
    TradePayloadBuilderService,
)
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
        asset: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        ohlcv: bool | None = False,
    ) -> pd.DataFrame | OpenHighLowCloseVolume:
        try:
            subject = NatsSubjects.MARKETDATA_TRADE_REQUEST.value
            payload = self.trade_payload_builder_service.trade_payload_builder(
                ticker=ticker,
                asset=asset,
                start_time=start_time,
                end_time=end_time,
                ohlcv=ohlcv,
            )
            message = self.trade_parser_service.encode_trades(message=payload)
            response = await self.nats_client.request(subject, message, timeout=20)
            if ohlcv is False:
                return self.trade_parser_service.parse_trades_to_dataframe(response)
            else:
                return self.trade_parser_service.decode_open_high_low_closed_volume(
                    response
                )
        except Exception as e:
            self.logger.error(
                f"Error trying to fetch trades for timerange provided. start_time: {start_time}, end_time: {end_time}, due: {e}"
            )
            raise e
