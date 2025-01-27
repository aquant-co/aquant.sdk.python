from sqlalchemy import Column, String
from app.infra.database.models.base import Base

class PermissionModel(Base):
    __tablename__ = "permissions"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
