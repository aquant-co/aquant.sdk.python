from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class OpenHighLowCloseVolume:
    """Lightweight OpenHighLowCloseVolume data model for HFT pipelines."""

    ticker: str
    timestamp: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float

    def __repr__(self) -> str:
        return (
            f"OpenHighLowCloseVolume(ticker={self.ticker!r}, ts={self.timestamp!r}, "
            f"o={self.open_price}, h={self.high_price}, "
            f"l={self.low_price}, c={self.close_price}, v={self.volume})"
        )
