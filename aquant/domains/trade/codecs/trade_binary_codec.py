import struct
from datetime import datetime
from decimal import Decimal

import numpy as np
import pandas as pd

from aquant.core.logger import Logger
from aquant.domains.trade.entity import Trade


class TradeBinaryCodec:
    __slots__ = ("_struct", "_encode_buffer", "_logger")
    FORMAT = "=10s10s15sqddccII"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, logger: Logger) -> None:
        self._struct = struct.Struct(self.FORMAT)
        self._encode_buffer = bytearray(self.SIZE)
        self._logger = logger

    def decode(self, data: bytes) -> Trade:
        if len(data) != self.SIZE:
            raise ValueError(f"Invalid size: expected {self.SIZE}, got {len(data)}")

        tkr_b, ast_b, fk_b, ts_ns, price_f, quantity_f, side_b, td_b, sid, bid = (
            self._struct.unpack(data)
        )

        tkr = tkr_b.rstrip(b"\x00").decode("ascii")
        ast = ast_b.rstrip(b"\x00").decode("ascii")
        fk = fk_b.rstrip(b"\x00").decode("ascii")
        side = side_b.decode("ascii")
        td = td_b.decode("ascii")
        ev_time = datetime.fromtimestamp(ts_ns / 1e9)
        price = Decimal(price_f)
        qty = Decimal(quantity_f)

        return Trade(
            ticker=tkr or None,
            asset=ast or None,
            fk_order_id=fk or None,
            event_time=ev_time,
            price=price,
            quantity=qty,
            side=side,
            tick_direction=td,
            seller_id=sid,
            buyer_id=bid,
        )

    def decode_trades(self, data: bytes) -> list[Trade]:
        """
        Decode a stream of binary-encoded Trade records.
        Returns one Trade per SIZE-byte chunk.
        """
        total = len(data)
        if total < self.SIZE:
            self._logger.warning(
                f"Received {total} bytes—too small for a single Trade record"
            )
            return []
        if total % self.SIZE != 0:
            self._logger.error(f"Data length {total} not a multiple of {self.SIZE}")
            raise ValueError(f"Data length {total} is not a multiple of {self.SIZE}")

        mv = memoryview(data)
        count = total // self.SIZE
        trades: list[Trade] = []

        for i in range(count):
            chunk = mv[i * self.SIZE : (i + 1) * self.SIZE]
            (tkr_b, ast_b, fk_b, ts_ns, price_f, quantity_f, side_b, td_b, sid, bid) = (
                self._struct.unpack(chunk)
            )

            tkr = tkr_b.rstrip(b"\x00").decode("ascii") or None
            ast = ast_b.rstrip(b"\x00").decode("ascii") or None
            fk = fk_b.rstrip(b"\x00").decode("ascii") or None
            side = side_b.decode("ascii")
            td = td_b.decode("ascii")
            ev_time = datetime.fromtimestamp(ts_ns / 1e9)
            price = Decimal(str(price_f))
            qty = Decimal(str(quantity_f))

            trade = Trade(
                ticker=tkr,
                asset=ast,
                fk_order_id=fk,
                event_time=ev_time,
                price=price,
                quantity=qty,
                side=side,
                tick_direction=td,
                seller_id=sid,
                buyer_id=bid,
            )
            self._logger.debug(f"Decoded trade #{i+1}: {trade!r}")
            trades.append(trade)
        self._logger.debug(f"Decoded {len(trades)} trades from {total} bytes")
        return trades

    def parse_trades_binary_to_dataframe(self, binary_data: bytes) -> pd.DataFrame:
        """
        Decodes a bytes array contendo N registros sequenciais no formato:
        - 20s   ticker (ASCII padded)
        - 20s   asset  (ASCII padded)
        - 20s   fk_order_id (ASCII padded)
        - Q     event_time (uint64 nanoseconds since epoch)
        - 50s   price_ascii (ASCII padded)
        - d     quantity (float64)
        - 1s    side (ASCII)
        - 1s    tick_direction (ASCII)
        - I     seller_id (uint32)
        - I     buyer_id  (uint32)
        Retorna um DataFrame com colunas:
        ticker, asset, fk_order_id, buyer_id, seller_id,
        price (float), quantity, side, tick_direction, event_time (datetime64[ns]).
        """
        n = len(binary_data)
        self._logger.debug(f"Received {n} bytes of binary trade-data.")

        dtype = np.dtype(
            [
                ("ticker", "S20"),
                ("asset", "S20"),
                ("fk_order_id", "S20"),
                ("event_time", ">u8"),
                ("price_ascii", "S50"),
                ("quantity", ">f8"),
                ("side", "S1"),
                ("tick_direction", "S1"),
                ("seller_id", ">u4"),
                ("buyer_id", ">u4"),
            ]
        )
        rec_size = dtype.itemsize
        if n % rec_size != 0:
            self._logger.warning(
                f"{n} bytes não é múltiplo de {rec_size}, truncando extras."
            )
        count = n // rec_size

        arr = np.frombuffer(binary_data, dtype=dtype, count=count)
        arr = arr.astype(arr.dtype.newbyteorder("="))

        tickers = np.char.decode(arr["ticker"], "ascii")
        tickers = np.char.rstrip(tickers, "\x00")
        assets = np.char.decode(arr["asset"], "ascii")
        assets = np.char.rstrip(assets, "\x00")
        fk_ids = np.char.decode(arr["fk_order_id"], "ascii")
        fk_ids = np.char.rstrip(fk_ids, "\x00")
        prices_ascii = np.char.decode(arr["price_ascii"], "ascii")
        prices_ascii = np.char.rstrip(prices_ascii, "\x00")
        sides = np.char.decode(arr["side"], "ascii")
        tdirs = np.char.decode(arr["tick_direction"], "ascii")

        df = pd.DataFrame(
            {
                "ticker": tickers,
                "asset": assets,
                "fk_order_id": fk_ids,
                "buyer_id": arr["buyer_id"],
                "seller_id": arr["seller_id"],
                "price": pd.to_numeric(prices_ascii, errors="coerce"),
                "quantity": arr["quantity"],
                "side": sides,
                "tick_direction": tdirs,
                "event_time": pd.to_datetime(arr["event_time"], unit="ns"),
            }
        )

        self._logger.debug(f"Parsed {len(df)} trades into DataFrame.")
        return df
