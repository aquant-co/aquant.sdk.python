import struct
from datetime import UTC, datetime

from aquant.core.logger import Logger
from aquant.domains.trade.dtos import TradeDTO, TradeParamsDTO
from aquant.domains.trade.utils.enums import Actions, TimescaleIntervalEnum


class TradeBinaryRequestCodec:
    """
    Wire format (fixed‐width):
      32s   action      (ASCII, e.g. "GET_TRADES_BY_TICKER_AND_TIMERANGE")
      32s   interval    (ASCII, e.g. "MINUTE_15", or empty)
      10s   ticker      (ASCII, padded)
      10s   asset       (ASCII, padded)
      Q     start_time  (uint64 nanoseconds since epoch)
      Q     end_time    (uint64 nanoseconds since epoch)
    Total size: 32 + 32 + 10 + 10 + 8 + 8 = 100 bytes
    """

    __slots__ = ("_struct", "_buf", "_logger")

    FORMAT = "!64s16s10s10sQQ"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, logger: Logger) -> None:
        self._struct = struct.Struct(self.FORMAT)
        self._buf = bytearray(self.SIZE)
        self._logger = logger

    def _pack_str(self, s: str | None, length: int) -> bytes:
        b = (s or "").encode("ascii", "ignore")[:length]
        return b.ljust(length, b"\x00")

    def _ts_ns(self, dt: datetime | None) -> int:
        if not dt:
            return 0

        if dt.tzinfo is None:
            dt_utc = dt.replace(tzinfo=UTC)
        else:
            dt_utc = dt.astimezone(UTC)

        epoch = datetime(1970, 1, 1, tzinfo=UTC)
        delta = dt_utc - epoch
        return (
            delta.days * 86_400 * 1_000_000_000
            + delta.seconds * 1_000_000_000
            + delta.microseconds * 1_000
        )

    def encode(self, dto: TradeDTO) -> bytes:
        raw_action = dto.action
        action_str = raw_action.name if hasattr(raw_action, "name") else str(raw_action)
        action_b = self._pack_str(action_str, 64)
        raw_int = dto.params.interval
        interval_str = (
            raw_int.name
            if hasattr(raw_int, "name")
            else (str(raw_int) if raw_int else "")
        )
        interval_b = self._pack_str(interval_str, 16)
        ticker_b = self._pack_str(dto.params.ticker, 10)
        asset_b = self._pack_str(dto.params.asset, 10)
        start_ns = self._ts_ns(dto.params.start_time)
        end_ns = self._ts_ns(dto.params.end_time)

        self._struct.pack_into(
            self._buf,
            0,
            action_b,
            interval_b,
            ticker_b,
            asset_b,
            start_ns,
            end_ns,
        )
        payload = bytes(self._buf)
        self._logger.debug(f"Encoded TradeDTO → {len(payload)} bytes")
        return payload

    def decode(self, data: bytes) -> TradeDTO:
        if len(data) != self.SIZE:
            raise ValueError(f"Bad payload size: {len(data)} != {self.SIZE}")

        act_b, int_b, tkr_b, ast_b, start_ns, end_ns = self._struct.unpack(data)
        action_str = act_b.rstrip(b"\x00").decode("ascii")
        interval_str = int_b.rstrip(b"\x00").decode("ascii")
        params = TradeParamsDTO(
            ticker=tkr_b.rstrip(b"\x00").decode("ascii") or None,
            interval=(
                TimescaleIntervalEnum[interval_str]
                if interval_str in TimescaleIntervalEnum.__members__
                else (TimescaleIntervalEnum(interval_str) if interval_str else None)
            ),
            asset=ast_b.rstrip(b"\x00").decode("ascii") or None,
            start_time=(
                datetime.fromtimestamp(start_ns / 1e9, tz=UTC) if start_ns else None
            ),
            end_time=(datetime.fromtimestamp(end_ns / 1e9, tz=UTC) if end_ns else None),
        )
        try:
            action = Actions[action_str]
        except KeyError:
            action = Actions(action_str)
        return TradeDTO(action=action, params=params)
