from pydantic import BaseModel, Field


class OpenHighLowCloseVolume(BaseModel):
    open: float = Field(alias="open")
    high: float
    low: float
    close: float
    volume: float

    class Config:
        from_attributes: True
