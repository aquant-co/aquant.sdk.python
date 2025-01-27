from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from uuid import UUID, uuid4
from typing import Optional, List

from app.core.logger.logger_interface import LoggerInterface
from app.core.exceptions.repositories import RepositoryError
from app.domains.role.interfaces import RoleRepositoryInterface
from app.infra.database.models import RoleModel
from app.domains.role.entities import Role


class RoleRepository(RoleRepositoryInterface):
    """
    Concrete implementation of RoleRepositoryInterface using SQLAlchemy.
    """

    def __init__(self, session: AsyncSession, logger: LoggerInterface) -> None:
        self.session = session
        self.logger = logger

    async def create_role(self, name: str, description: str) -> UUID:
        """
        Creates a new role in the database.
        """
        try:
            role_id = uuid4()
            await self.session.execute(
                insert(RoleModel).values(
                    id=role_id,
                    name=name,
                    description=description,
                )
            )
            await self.session.commit()
            self.logger.info(f"Role '{name}' created successfully with ID {role_id}.")
            return role_id
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Failed to create role '{name}': {e}")
            raise RepositoryError(f"Failed to create role '{name}'.", details=str(e))

    async def get_role_by_id(self, role_id: UUID) -> Optional[Role]:
        """
        Retrieves a role by its ID.
        """
        try:
            result = await self.session.execute(
                select(RoleModel).where(RoleModel.id == role_id)
            )
            role = result.scalars().first()
            return Role.model_validate(role) if role else None
        except Exception as e:
            self.logger.error(f"Failed to retrieve role by ID '{role_id}': {e}")
            raise RepositoryError(f"Failed to retrieve role by ID '{role_id}'.", details=str(e))

    async def get_role_by_name(self, name: str) -> Optional[Role]:
        """
        Retrieves a role by its name.
        """
        try:
            result = await self.session.execute(
                select(RoleModel).where(RoleModel.name == name)
            )
            role = result.scalars().first()
            return Role.model_validate(role) if role else None
        except Exception as e:
            self.logger.error(f"Failed to retrieve role by name '{name}': {e}")
            raise RepositoryError(f"Failed to retrieve role by name '{name}'.", details=str(e))

    async def list_roles(self) -> List[Role]:
        """
        Lists all roles in the database.
        """
        try:
            result = await self.session.execute(select(RoleModel))
            roles = result.scalars().all()
            self.logger.info(f"Retrieved {len(roles)} roles from the database.")
            return [Role.model_validate(role) for role in roles]
        except Exception as e:
            self.logger.error(f"Failed to list roles: {e}")
            raise RepositoryError("Failed to list roles.", details=str(e))
