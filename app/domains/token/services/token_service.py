from datetime import UTC, datetime, timedelta
from uuid import UUID

from app.core.exceptions.app import AppError
from app.core.logger.logger_interface import LoggerInterface
from app.core.utils.token_manager import decode_jwt, generate_jwt
from app.domains.token.entities import Token
from app.domains.token.interfaces import TokenRepositoryInterface
from app.domains.token.schemas.token_schemas import JWTTokenPayload


class TokenService:
    """
    Service for managing tokens.
    """

    def __init__(self, token_repo: TokenRepositoryInterface, logger: LoggerInterface):
        self.token_repo = token_repo
        self.logger = logger

    async def generate_jwt_with_payload(
        self,
        sub: UUID,
        username: str,
        email: str,
        roles: list[str],
        permissions: list[str],
        organization_id: UUID,
        organization_name: str,
        session_id: UUID,
        ip_address: str,
        device_id: str,
        custom_claims: dict = None,
    ) -> str:
        """
        Generates a JWT using the defined JWTPayload schema.

        Args:
            sub (UUID): User ID (subject).
            username (str): Username.
            email (str): Email.
            roles (list[str]): List of user roles.
            permissions (list[str]): List of user permissions.
            organization_id (UUID): Organization ID.
            organization_name (str): Organization name.
            session_id (UUID): Unique session ID.
            ip_address (str): User's IP address.
            device_id (str): User's device ID.
            custom_claims (dict): Additional custom claims (optional).

        Returns:
            str: The generated JWT.
        """
        iat = datetime.now(UTC)
        exp = iat + timedelta(hours=1)  # 1-hour token validity

        payload = JWTTokenPayload(
            sub=sub,
            username=username,
            email=email,
            roles=roles,
            permissions=permissions,
            organization_id=organization_id,
            organization_name=organization_name,
            session_id=session_id,
            ip_address=ip_address,
            device_id=device_id,
            iat=iat,
            exp=exp,
            auth_time=iat,
            metadata={
                "department": "Engineering",
                "preferred_language": "en",
                "timezone": "UTC+0",
            },
            custom_claims=custom_claims or {},
        )
        return generate_jwt(payload.dict())

    async def generate_token(
        self, user_id: UUID, payload: dict, expires_in: timedelta | None = None
    ) -> Token:
        """
        Generates a new JWT token.

        Args:
            user_id (UUID): The ID of the user.
            payload (dict): The token payload.
            expires_in (Optional[timedelta]): Token expiration duration.

        Returns:
            Token: The generated token entity.
        """
        try:
            expires_in = expires_in or timedelta(hours=1)
            payload["exp"] = datetime.now(UTC) + expires_in
            token_str = generate_jwt(payload)

            token = Token(
                user_id=user_id,
                token=token_str,
                expires_at=payload["exp"],
                created_at=datetime.now(UTC),
            )
            await self.token_repo.create_token(token)

            self.logger.info(f"Generated token for user ID: {user_id}.")
            return token
        except Exception as e:
            self.logger.error(f"Error generating token for user ID {user_id}: {e}")
            raise AppError("Failed to generate token.") from e

    async def validate_token(self, token_str: str) -> bool:
        """
        Validates a token.

        Args:
            token_str (str): The JWT token.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            decoded = decode_jwt(token_str)

            if not await self.token_repo.is_token_valid(token_str):
                self.logger.warning("Token is invalid or revoked.")
                return False

            if decoded["exp"] < datetime.now(UTC):
                self.logger.warning("Token has expired.")
                return False

            self.logger.info("Token is valid.")
            return True
        except Exception as e:
            self.logger.warning(f"Token validation failed: {e}")
            return False

    async def revoke_token(self, token_id: UUID, reason: str | None = None) -> None:
        """
        Revokes a token.

        Args:
            token_id (UUID): The ID of the token.
            reason (Optional[str]): The reason for revocation.
        """
        try:
            await self.token_repo.revoke_token(token_id, reason)
            self.logger.info(
                f"Token {token_id} revoked. Reason: {reason or 'No reason provided'}."
            )
        except Exception as e:
            self.logger.error(f"Error revoking token {token_id}: {e}")
            raise AppError("Failed to revoke token.") from e

    async def list_user_tokens(self, user_id: UUID) -> list[Token]:
        """
        Lists all tokens for a user.

        Args:
            user_id (UUID): The ID of the user.

        Returns:
            List[Token]: A list of token entities.
        """
        try:
            tokens = await self.token_repo.get_tokens_by_user_id(user_id)
            self.logger.info(f"Listed {len(tokens)} tokens for user ID {user_id}.")
            return tokens
        except Exception as e:
            self.logger.error(f"Error listing tokens for user ID {user_id}: {e}")
            raise AppError("Failed to list tokens.") from e
