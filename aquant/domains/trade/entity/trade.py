from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal


@dataclass(slots=True)
class Trade:
    """Lightweight Trade data model."""

    ticker: str | None
    asset: str | None
    fk_order_id: str | None
    event_time: datetime
    price: Decimal
    quantity: Decimal
    side: Literal["B", "S"] | None
    tick_direction: str | None
    seller_id: int
    buyer_id: int

    def __repr__(self) -> str:
        return (
            f"Trade(ticker={self.ticker!r}, asset={self.asset!r}, "
            f"fk_order_id={self.fk_order_id!r}, event_time={self.event_time!r}, "
            f"price={self.price!r}, quantity={self.quantity!r}, "
            f"side={self.side!r}, tick_direction={self.tick_direction!r}, "
            f"seller_id={self.seller_id}, buyer_id={self.buyer_id})"
        )
