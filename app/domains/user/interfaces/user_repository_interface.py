from uuid import UUID
from abc import ABC, abstractmethod
from typing import Optional, List

from app.domains.user.entities.user import User


class UserRepositoryInterface(ABC):
    """
    Interface para o repositório de usuários. Define os métodos que qualquer implementação deve fornecer.
    """
    @abstractmethod
    async def get_user(self, username: str) -> Optional[User]:
        """
        Obtém um usuário pelo nome de usuário.

        Args:
            username (str): O nome de usuário.

        Returns:
            Optional[User]: O usuário encontrado, ou None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Obtém um usuário pelo ID.

        Args:
            user_id (UUID): O ID do usuário.

        Returns:
            Optional[User]: O usuário encontrado, ou None.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get_user_permissions(self, user_id: UUID) -> Optional[List[str]]:
        """
        Obtém as permissões do usuário.

        Args:
            user_id (UUID): O ID do usuário.

        Returns:
            List[str]: Lista de permissões do usuário.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtém um usuário pelo email.

        Args:
            email (str): O email do usuário.

        Returns:
            Optional[User]: O usuário encontrado, ou None.
        """
        raise NotImplementedError

    @abstractmethod
    async def save(self, user: User) -> None:
        """
        Salva ou atualiza um usuário no banco de dados.

        Args:
            user (User): A entidade de usuário a ser salva.

        Returns:
            User: A entidade de usuário após ser salva.
        """
        raise NotImplementedError
