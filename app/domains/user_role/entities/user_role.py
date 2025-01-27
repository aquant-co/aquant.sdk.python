from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class UserRole(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    role_id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    deleted_at: datetime = None

    def prepare_for_database(self) -> None:
        """
        Prepare the entity for database insertion.
        """
        self.updated_at = datetime.now(UTC)

    class Config:
        from_attributes = True
