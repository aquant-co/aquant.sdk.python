from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List

class Role(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    permissions: List[UUID] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime = Field(default=None, nullable=True) #type: ignore

    class Config:
        from_attributes = True

    def add_permission(self, permission_id: UUID):
        """
        Adds a permission to the role.

        Args:
            permission_id (UUID): The ID of the permission to add.
        """
        if permission_id not in self.permissions:
            self.permissions.append(permission_id)

    def remove_permission(self, permission_id: UUID):
        """
        Removes a permission from the role.

        Args:
            permission_id (UUID): The ID of the permission to remove.
        """
        if permission_id in self.permissions:
            self.permissions.remove(permission_id)

    def soft_delete(self):
        """
        Marks the role as deleted by setting `deleted_at` to the current time.
        """
        self.deleted_at = datetime.now(timezone.utc)

    def is_deleted(self) -> bool:
        """
        Checks if the role is marked as deleted.

        Returns:
            bool: True if the role is deleted, False otherwise.
        """
        return self.deleted_at is not None
