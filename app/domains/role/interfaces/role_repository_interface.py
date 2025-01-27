from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domains.role.entities import Role

class RoleRepositoryInterface(ABC):
    """
    Interface for Role Repository
    """

    @abstractmethod
    async def create_role(self, name: str, description: str) -> UUID:
        """
        Creates a new role.

        Args:
            name (str): The name of the role.
            description (str): The description of the role.

        Returns:
            UUID: The ID of the created role.
        """
        pass

    @abstractmethod
    async def get_role_by_id(self, role_id: UUID) -> Optional[Role]:
        """
        Retrieves a role by its ID.

        Args:
            role_id (UUID): The ID of the role.

        Returns:
            Optional[Role]: The role data if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_role_by_name(self, name: str) -> Optional[Role]:
        """
        Retrieves a role by its name.

        Args:
            name (str): The name of the role.

        Returns:
            Optional[Role]: The role data if found, otherwise None.
        """
        pass

    @abstractmethod
    async def list_roles(self) -> list[Role]:
        """
        Lists all roles.

        Returns:
            list[dict[str, Any]]: A list of roles.
        """
        pass
