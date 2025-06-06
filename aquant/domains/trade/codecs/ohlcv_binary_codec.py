import struct
from datetime import datetime

import numpy as np
import pandas as pd

from aquant.core.logger import Logger
from aquant.domains.trade.entity import OpenHighLowCloseVolume


class OpenHighLowCloseVolumeBinaryCodec:
    """
    Codec for encoding/decoding Open (OpenHighLowCloseVolume) objects to/from binary
    but for business logic it'll only be a decoder method

    Binary layout:
      10s       ticker (ASCII, null-padded)
      q         timestamp, int64 nanoseconds since epoch
      dddddd    open, high, low, close, volume (float64 each)
    Total size = 10 + 8 + 8*5 = 58 bytes
    """

    __slots__ = ("_struct", "_logger")
    FORMAT = "=10sqddddd"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, logger: Logger) -> None:
        self._struct = struct.Struct(self.FORMAT)
        self._logger = logger

    def decode_list(self, data: bytes) -> list[OpenHighLowCloseVolume]:
        total = len(data)
        if total < self.SIZE or total % self.SIZE != 0:
            self._logger.error(
                f"Invalid OpenHighLowCloseVolume blob size {total}, must be multiple of {self.SIZE}"
            )
            raise ValueError(
                f"Invalid OpenHighLowCloseVolume blob size {total}, must be multiple of {self.SIZE}"
            )
        mv = memoryview(data)
        n = total // self.SIZE
        out: list[OpenHighLowCloseVolume] = []
        for i in range(n):
            start = i * self.SIZE
            tkr_b, ts_ns, open, high, low, close, volume = self._struct.unpack(
                mv[start : start + self.SIZE]
            )
            ticker = tkr_b.rstrip(b"\x00").decode("ascii")
            ts = datetime.fromtimestamp(ts_ns / 1e9)
            out.append(
                OpenHighLowCloseVolume(ticker, ts, open, high, low, close, volume)
            )
        return out

    def parse_ohlcv_binary_into_dataframe(self, blob: bytes) -> pd.DataFrame:
        dtype = np.dtype(
            [
                ("ticker", "S10"),
                ("timestamp", "<u8"),
                ("open", "f8"),
                ("high", "f8"),
                ("low", "f8"),
                ("close", "f8"),
                ("volume", "f8"),
            ]
        )
        arr = np.frombuffer(blob, dtype=dtype)
        df = pd.DataFrame(arr)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ns")
        tickers = np.char.decode(arr["ticker"], encoding="ascii")
        tickers = np.char.rstrip(tickers, "\x00")
        df["ticker"] = tickers

        return df
