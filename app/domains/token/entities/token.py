from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class Token(BaseModel): 
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    token: str
    revoked: bool = False
    revoked_reason: Optional[str] = None
    revoked_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True