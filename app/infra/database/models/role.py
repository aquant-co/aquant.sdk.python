from sqlalchemy import Column, String
from app.infra.database.models.base import Base

class RoleModel(Base):
    __tablename__ = "roles"

    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
