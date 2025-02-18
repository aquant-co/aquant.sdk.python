from datetime import UTC, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class Trade(BaseModel):
    ticker: str | None
    asset: str | None
    fk_order_id: str | None = Field(
        ...,
        description="External order id of the trade informed by the stock exchange integration system",
    )
    event_time: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp of the trade used for time-series analysis",
    )
    price: Decimal = Field(..., description="The trade price")
    quantity: Decimal = Field(..., description="The quantity traded in this movement")
    side: str | None = Field(
        ...,
        min_length=1,
        max_length=1,
        description='Indicates if the trade is a "Buy" (B) or "Sell" (S)',
    )
    tick_direction: str | None | None = Field(
        None,
        min_length=1,
        max_length=1,
        description="Refers to the movement of a stock's price",
    )
    seller_id: int = Field(
        ..., description="Represents the broker responsible for selling the stock"
    )
    buyer_id: int = Field(
        ..., description="Represents the broker responsible for buying the stock"
    )

    class Config:
        from_attributes = True
        orm_mode: True
