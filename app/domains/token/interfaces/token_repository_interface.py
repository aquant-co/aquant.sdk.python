from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from app.domains.token.entities import Token

class TokenRepositoryInterface(ABC):
    """Token repository interface"""

    @abstractmethod
    async def create_token(self, token: Token) -> Optional[Token]:
        """Creates a new token in the database."""
        raise NotImplementedError

    @abstractmethod
    async def get_token(self, token_str: str) -> Optional[Token]:
        """Gets a token by its string value."""
        raise NotImplementedError

    @abstractmethod
    async def revoke_token(self, token_id: UUID, reason: Optional[str] = None) -> None:
        """Revokes a token with an optional reason."""
        raise NotImplementedError

    @abstractmethod
    async def get_tokens_by_user_id(self, user_id: UUID) -> Optional[List[Token]]:
        """Gets all tokens associated with a specific user."""
        raise NotImplementedError

    @abstractmethod
    async def is_token_valid(self, token_str: str) -> bool:
        """Checks if a token is valid (not expired and not revoked)."""
        raise NotImplementedError

    @abstractmethod
    async def update_token(self, token_id: UUID, new_expiration: Optional[datetime] = None) -> None:
        """
        Updates a token, for example by renewing its expiration time.

        Args:
            token_id (UUID): ID of the token to update.
            new_expiration (Optional[datetime]): New expiration time as a datetime object.
        """
        raise NotImplementedError

    @abstractmethod
    async def check_expiration(self, token_id: UUID) -> bool:
        """
        Checks if a token has expired.

        Args:
            token_id (UUID): ID of the token to check.

        Returns:
            bool: True if the token is valid, False if expired.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_expired_tokens(self) -> None:
        """
        Deletes all expired tokens from the database.
        Useful for periodic cleanup routines.
        """
        raise NotImplementedError
