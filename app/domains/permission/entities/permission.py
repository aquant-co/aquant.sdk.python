from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Permission(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
