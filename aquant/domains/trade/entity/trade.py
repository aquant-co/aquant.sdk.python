from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trade:
    symbol: str
    price: float
    quantity: int
    timestamp: datetime
