from dataclasses import dataclass
from datetime import datetime

from aquant.domains.trade.utils.enums import Actions, TimescaleIntervalEnum


@dataclass(slots=True)
class TradeParamsDTO:
    ticker: str | None
    interval: TimescaleIntervalEnum | None
    asset: str | None
    start_time: datetime
    end_time: datetime


@dataclass(slots=True)
class TradeDTO:
    action: Actions
    params: TradeParamsDTO
