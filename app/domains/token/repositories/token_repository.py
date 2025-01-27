from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.domains.token.entities import Token
from app.domains.token.interfaces import TokenRepositoryInterface
from app.infra.database.models import TokenModel
from app.core.logger.logger_interface import LoggerInterface
from app.core.exceptions.repositories import RepositoryError


class TokenRepository(TokenRepositoryInterface):
    """Concrete implementation of the Token repository interface."""

    def __init__(self, session: AsyncSession, logger: LoggerInterface) -> None:
        self.session = session
        self.logger = logger

    async def create_token(self, token: Token) -> Optional[Token]:
        """Creates a new token in the database."""
        try:
            token_model = TokenModel(**token.model_dump())
            self.session.add(token_model)
            await self.session.commit()
            await self.session.refresh(token_model)
            return Token.model_validate(token_model)
        except Exception as e:
            self.logger.error(f"Error creating token: {e}")
            await self.session.rollback()
            raise RepositoryError("Failed to create token in the database.", str(e), self.logger)

    async def get_token(self, token_str: str) -> Optional[Token]:
        """Gets a token by its string value."""
        try:
            result = await self.session.execute(select(TokenModel).where(TokenModel.token == token_str))
            token_model = result.scalars().first()
            return Token.model_validate(token_model) if token_model else None
        except Exception as e:
            self.logger.error(f"Error fetching token: {e}")
            raise RepositoryError("Failed to fetch token from the database.", str(e), self.logger)

    async def revoke_token(self, token_id: UUID, reason: Optional[str] = None) -> None:
        """Revokes a token with an optional reason."""
        try:
            await self.session.execute(
                update(TokenModel)
                .where(TokenModel.id == token_id)
                .values(revoked=True, revoked_at=datetime.now(timezone.utc), revoked_reason=reason)
            )
            await self.session.commit()
        except Exception as e:
            self.logger.error(f"Error revoking token {token_id}: {e}")
            await self.session.rollback()
            raise RepositoryError("Failed to revoke token in the database.", str(e), self.logger)

    async def get_tokens_by_user_id(self, user_id: UUID) -> List[Token]:
        """Gets all tokens associated with a specific user."""
        try:
            result = await self.session.execute(select(TokenModel).where(TokenModel.user_id == user_id))
            token_models = result.scalars().all()
            return [Token.model_validate(token) for token in token_models]
        except Exception as e:
            self.logger.error(f"Error fetching tokens for user {user_id}: {e}")
            raise RepositoryError("Failed to fetch tokens for the user.", str(e), self.logger)

    async def is_token_valid(self, token_str: str) -> bool:
        """Checks if a token is valid (not expired and not revoked)."""
        try:
            token = await self.get_token(token_str)
            if not token or token.revoked or token.expires_at < datetime.now(timezone.utc):
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error checking token validity: {e}")
            raise RepositoryError("Failed to check token validity.", str(e), self.logger)

    async def update_token(self, token_id: UUID, new_expiration: Optional[datetime] = None) -> None:
        """Updates a token, e.g., by renewing its expiration time."""
        try:
            new_expiration = new_expiration or datetime.now(timezone.utc) + timedelta(days=7)
            await self.session.execute(
                update(TokenModel)
                .where(TokenModel.id == token_id)
                .values(expires_at=new_expiration, updated_at=datetime.now(timezone.utc))
            )
            await self.session.commit()
        except Exception as e:
            self.logger.error(f"Error updating token {token_id}: {e}")
            await self.session.rollback()
            raise RepositoryError(
                "Failed to update token in the database.",
                details=str(e),
                logger=self.logger,
            )

    async def check_expiration(self, token_id: UUID) -> bool:
        """Checks if a token has expired."""
        try:
            result = await self.session.execute(select(TokenModel).where(TokenModel.id == token_id))
            token_model = result.scalars().first()
            
            if not token_model:
                self.logger.info(f"Token {token_id} not found.")
                return False
            
            current_time = datetime.now(timezone.utc)
            is_valid = token_model.expires_at >= current_time

            self.logger.debug(f"Token {token_id} expiration check: {is_valid}")
            return bool(is_valid)
        except Exception as e:
            self.logger.error(f"Error checking expiration for token {token_id}: {e}")
            raise RepositoryError("Failed to check token expiration.", str(e), self.logger)
            
    async def delete_expired_tokens(self) -> None:
        """Deletes all expired tokens from the database."""
        try:
            await self.session.execute(delete(TokenModel).where(TokenModel.expires_at < datetime.now(timezone.utc)))
            await self.session.commit()
        except Exception as e:
            self.logger.error(f"Error deleting expired tokens: {e}")
            await self.session.rollback()
            raise RepositoryError("Failed to delete expired tokens.", str(e), self.logger)
