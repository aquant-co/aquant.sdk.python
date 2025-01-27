from datetime import datetime, timezone
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, DateTime
import uuid
from sqlalchemy.dialects.postgresql import UUID


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def id(cls):
        return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False,
        )

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True)
    
from app.infra.database.models.user import UserModel # type: ignore
from app.infra.database.models.role import RoleModel # type: ignore
from app.infra.database.models.permission import PermissionModel # type: ignore
from app.infra.database.models.user_roles import UserRoleModel # type: ignore
from app.infra.database.models.role_permission import RolePermissionModel # type: ignore
from app.infra.database.models.token import TokenModel # type: ignore
