from datetime import datetime
from decimal import Decimal

from pydantic import ConfigDict, Field, model_validator
from pydantic.dataclasses import dataclass


@dataclass(
    config=ConfigDict(
        frozen=True,
        slots=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat(), Decimal: lambda v: str(v)},
        json_schema_extra={
            "example": {
                "ticker": "AAPL",
                "timestamp": "2023-10-01T00:00:00Z",
                "open_price": "150.00",
                "high_price": "155.00",
                "low_price": "149.00",
                "close_price": "154.00",
                "volume": "1000000",
            }
        },
    )
)
class OpenHighLowCloseVoume:
    """Open High Low Close Volume (OHLCV) data model."""

    ticker: str = Field(..., description="ticker symbol")
    timestamp: datetime = Field(..., description="timestamp of the OHLCV data")
    open_price: Decimal = Field(..., description="'open' price")
    high_price: Decimal = Field(..., description="'close' price")
    low_price: Decimal = Field(..., description="'low' price")
    close_price: Decimal = Field(..., description="'close' price")
    volume: Decimal = Field(..., description="'volume' quantity")

    @model_validator(mode="after")
    @classmethod
    def check_price_consistency(
        cls, model: "OpenHighLowCloseVoume"
    ) -> "OpenHighLowCloseVoume":
        open_price, high_price, low_price, close_price = (
            model.open_price,
            model.high_price,
            model.low_price,
            model.close_price,
        )
        if high_price <= max(open_price, close_price):
            raise ValueError("High price must be >= max(open_price, close_price)")
        if low_price >= min(open_price, close_price):
            raise ValueError("Low price must be <= min(open_price, close_price)")
