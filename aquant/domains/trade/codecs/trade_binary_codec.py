import struct
from datetime import datetime
from decimal import Decimal

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
