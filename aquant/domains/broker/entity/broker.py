from pydantic import BaseModel, ConfigDict


class Broker(BaseModel):
    id: int
    fk_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
