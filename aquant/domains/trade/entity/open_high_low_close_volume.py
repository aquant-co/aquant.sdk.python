from pydantic import BaseModel, Field


class OpenHighLowClosedVolume(BaseModel):
    ticker: str
    asset: str
    open: float = Field(alias="open")
    high: float
    low: float
    close: float
    volume: float

    class Config:
        from_attributes: True
