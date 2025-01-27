from uuid import UUID

from app.core.exceptions.app import AppError
from app.core.logger.logger_interface import LoggerInterface
from app.core.utils.token_manager import generate_jwt
from app.domains.user.entities import User
from app.domains.user.interfaces import UserRepositoryInterface


class UserService:
    def __init__(
        self, logger: LoggerInterface, user_repo: UserRepositoryInterface
    ) -> None:
        self.logger = logger
        self.user_repo = user_repo

    async def register_user(self, username: str, email: str, password: str) -> User:
        """
        Registers a new user in the system.

        Args:
            username (str): The username for the new user.
            email (str): The email for the new user.
            password (str): The plaintext password for the new user.

        Returns:
            User: The newly created user entity.
        """
        try:
            if await self.user_repo.get_by_email(email):
                raise AppError(
                    "Email is already registered.", details=f"Email: {email}"
                )

            if await self.user_repo.get_user(username):
                raise AppError(
                    "Username is already taken.", details=f"Username: {username}"
                )

            hashed_password = User.hash_password(password)
            user = User(username=username, email=email, hashed_password=hashed_password)

            await self.user_repo.save(user)

            self.logger.info(f"User '{username}' registered successfully.")
            return user
        except Exception as e:
            self.logger.error(f"Error registering user '{username}': {e}")
            raise AppError("Error during user registration.") from e

    async def authenticate_user(self, email: str, password: str) -> str | None:
        """
        Authenticates a user and returns a JWT if successful.

        Args:
            email (str): The email of the user.
            password (str): The plaintext password of the user.

        Returns:
            Optional[str]: The JWT if authentication is successful, otherwise None.
        """
        try:
            user = await self.user_repo.get_by_email(email)
            if not user or not user.verify_password(password):
                raise AppError("Invalid email or password.")

            payload = {
                "sub": str(user.id),
                "username": user.username,
                "email": user.email,
            }
            token = generate_jwt(payload)

            self.logger.info(f"User '{user.username}' authenticated successfully.")
            return token
        except AppError as e:
            self.logger.warning(f"Authentication failed for email '{email}': {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during authentication: {e}")
            raise AppError("Error during authentication.") from e

    async def get_user(self, user_id: UUID) -> User:
        """
        Retrieves a user by their ID.

        Args:
            user_id (UUID): The ID of the user to retrieve.

        Returns:
            User: The user entity if found.
        """
        try:
            user = await self.user_repo.get_user_by_id(user_id)
            if not user:
                raise AppError("User not found.", details=f"User ID: {user_id}")
            return user
        except Exception as e:
            self.logger.error(f"Error fetching user by ID '{user_id}': {e}")
            raise AppError("Error fetching user.") from e

    async def get_user_permissions(self, user_id: UUID) -> list[str] | None:
        """
        Retrieves the permissions for a user.

        Args:
            user_id (UUID): The ID of the user.

        Returns:
            List[str]: A list of permissions for the user.
        """
        try:
            permissions = await self.user_repo.get_user_permissions(user_id)
            self.logger.info(
                f"Permissions fetched for user ID '{user_id}': {permissions}"
            )
            return permissions
        except Exception as e:
            self.logger.error(
                f"Error fetching permissions for user ID '{user_id}': {e}"
            )
            raise AppError("Error fetching user permissions.") from e
