from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from datetime import datetime, timezone

from passlib.context import CryptContext

from app.core.config import Settings

settings = Settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

    @staticmethod
    def normalize_datetime(dt: datetime) -> datetime:
        """Convert a timezone-aware datetime to naive."""
        return dt.replace(tzinfo=None) if dt.tzinfo else dt

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)

    def prepare_for_database(self):
        """Prepare fields for database storage."""
        self.created_at = self.normalize_datetime(self.created_at)
        self.updated_at = self.normalize_datetime(self.updated_at)
