from uuid import UUID

from app.core.exceptions.app import AppError
from app.core.logger.logger_interface import LoggerInterface
from app.domains.role.entities import Role
from app.domains.role.interfaces import RoleRepositoryInterface


class RoleService:
    """
    Service for managing roles.
    """

    def __init__(self, role_repo: RoleRepositoryInterface, logger: LoggerInterface):
        self.role_repo = role_repo
        self.logger = logger

    async def create_role(self, name: str, description: str) -> Role:
        """
        Creates a new role.

        Args:
            name (str): The name of the role.
            description (str): The description of the role.

        Returns:
            Role: The created role.
        """
        try:
            existing_role = await self.role_repo.get_role_by_name(name)
            if existing_role:
                raise AppError(f"Role with name '{name}' already exists.")

            role_id = await self.role_repo.create_role(name, description)
            role = Role(id=role_id, name=name, description=description)
            self.logger.info(f"Role '{name}' created successfully.")
            return role
        except Exception as e:
            self.logger.error(f"Error creating role '{name}': {e}")
            raise AppError(f"Failed to create role '{name}'.") from e

    async def get_role_by_id(self, role_id: UUID) -> Role | None:
        """
        Retrieves a role by its ID.

        Args:
            role_id (UUID): The ID of the role.

        Returns:
            Optional[Role]: The role if found, otherwise None.
        """
        try:
            role = await self.role_repo.get_role_by_id(role_id)
            if not role:
                raise AppError(f"Role with ID '{role_id}' not found.")
            self.logger.info(f"Retrieved role by ID: {role_id}.")
            return role
        except Exception as e:
            self.logger.error(f"Error retrieving role by ID '{role_id}': {e}")
            raise AppError(f"Failed to retrieve role by ID '{role_id}'.") from e

    async def get_role_by_name(self, name: str) -> Role | None:
        """
        Retrieves a role by its name.

        Args:
            name (str): The name of the role.

        Returns:
            Optional[Role]: The role if found, otherwise None.
        """
        try:
            role = await self.role_repo.get_role_by_name(name)
            if not role:
                raise AppError(f"Role with name '{name}' not found.")
            self.logger.info(f"Retrieved role by name: {name}.")
            return role
        except Exception as e:
            self.logger.error(f"Error retrieving role by name '{name}': {e}")
            raise AppError(f"Failed to retrieve role by name '{name}'.") from e

    async def list_roles(self) -> list[Role]:
        """
        Lists all roles.

        Returns:
            List[Role]: A list of roles.
        """
        try:
            roles = await self.role_repo.list_roles()
            self.logger.info(f"Retrieved {len(roles)} roles.")
            return roles
        except Exception as e:
            self.logger.error(f"Error listing roles: {e}")
            raise AppError("Failed to list roles.") from e
