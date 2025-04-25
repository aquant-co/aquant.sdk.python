from datetime import datetime

from pydantic import BaseModel, Field

from aquant.domains.trade.utils.enums import Actions, TimescaleIntervalEnum


class TradeParamsDTO(BaseModel):
    ticker: str | None = Field(None, description="'ticker' of stock(security)")
    interval: TimescaleIntervalEnum | None = Field(
        None, description="'interval' of the timerange query"
    )
    asset: str | None = Field(
        None, description="'asset' is the description of stock(security)"
    )
    start_time: datetime | None = Field(
        None, description="'start_time' of the timerange query"
    )
    end_time: datetime | None = Field(
        None, description="'end_time' of the timerange query"
    )


class TradeDTO(BaseModel):
    action: Actions
    params: TradeParamsDTO
