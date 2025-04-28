from typing import Union

import pandas as pd

from aquant.core.logger import Logger
from aquant.domains.trade.codecs import (
    OpenHighLowCloseVolumeBinaryCodec,
    TradeBinaryCodec,
    TradeBinaryRequestCodec,
)
from aquant.domains.trade.dtos import TradeDTO
from aquant.domains.trade.entity import OpenHighLowCloseVolume, Trade

Parsed = Union[Trade, OpenHighLowCloseVolume]  # noqa: UP007


class TradeParserService:
    __slots__ = ("trade_codec", "trade_request_codec", "ohlcv_codec", "_logger")

    def __init__(
        self,
        logger: Logger,
        trade_codec: TradeBinaryCodec,
        trade_request_codec: TradeBinaryRequestCodec,
        ohlcv_codec: OpenHighLowCloseVolumeBinaryCodec,
    ) -> None:
        self._logger = logger
        self.trade_codec = trade_codec
        self.trade_request_codec = trade_request_codec
        self.ohlcv_codec = ohlcv_codec

    def encode(self, message: TradeDTO) -> bytes:
        return self.trade_request_codec.encode(message)

    def decode_trades_into_dataframe(self, message: bytes) -> pd.DataFrame:
        return self.trade_codec.parse_trades_binary_to_dataframe(message)

    def decode_ohlcv_into_dataframe(self, message: bytes) -> pd.DataFrame:
        return self.ohlcv_codec.parse_ohlcv_binary_into_dataframe(message)

    def decode(self, blob: bytes) -> list[Parsed]:
        size = len(blob)
        if size % self.trade_codec.SIZE == 0:
            return self.trade_codec.decode_trades(blob)
        if size % self.ohlcv_codec.SIZE == 0:
            return self.ohlcv_codec.decode_list(blob)
        raise ValueError(f"Blob length {size} is not a multiple of known record sizes")
