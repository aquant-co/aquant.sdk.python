import json
from datetime import datetime
from typing import Any
from uuid import UUID

from redis import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.repositories import RepositoryError
from app.core.logger.logger_interface import LoggerInterface
from app.domains.user.entities import User
from app.domains.user.interfaces import UserRepositoryInterface
from app.infra.database.models import (
    PermissionModel,
    RolePermissionModel,
    UserModel,
    UserRoleModel,
)
from app.infra.database.models.role import RoleModel


class UserRepository(UserRepositoryInterface):
    """
    Concrete implementation of UserRepositoryInterface using SQLAlchemy and Redis.
    """

    def __init__(
        self,
        postgres_session: AsyncSession,
        redis_session: Redis,
        logger: LoggerInterface,
    ) -> None:
        self.postgres_session = postgres_session
        self.redis_session = redis_session
        self.logger = logger
        self.redis_key_prefix = "aquant_auth_token:user"

    async def _get_redis_key(self, key: str) -> str | None:
        try:
            cached_value = await self.redis_session.get(key)
            if cached_value:
                self.logger.info(f"Cache hit for key: {key}")
            else:
                self.logger.info(f"Cache miss for key: {key}")
            return cached_value if cached_value else None
        except Exception as e:
            self.logger.error(f"Redis GET error for key '{key}': {e}")
            return None

    async def _set_redis_key(
        self, key: str, value: dict[Any, Any], ttl: int = 86400
    ) -> None:
        try:
            self.logger.info(f"Setting Redis key '{key}' with TTL {ttl}.")
            await self.redis_session.set(key, json.dumps(value, default=str), ex=ttl)
        except Exception as e:
            self.logger.error(f"Redis SET error for key '{key}': {e}")

    async def get_by_email(self, email: str) -> User | None:
        redis_key = f"{self.redis_key_prefix}:email:{email}"
        try:
            cached_user = await self._get_redis_key(redis_key)
            if cached_user:
                return User.model_validate(json.loads(cached_user))

            result = await self.postgres_session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            user_model = result.scalars().first()
            if user_model:
                user = User.model_validate(user_model)
                await self._set_redis_key(redis_key, user.model_dump())
                return user
            return None
        except Exception as e:
            self.logger.error(f"Error fetching user by email '{email}': {e}")
            raise RepositoryError(
                "Failed to get user by email from the database",
                details=str(e),
                logger=self.logger,
            ) from e

    async def get_user_permissions(self, user_id: UUID) -> list[str] | None:
        redis_key = f"{self.redis_key_prefix}:{user_id}:permissions"
        try:
            cached_permissions = await self._get_redis_key(redis_key)
            if cached_permissions:
                return json.loads(cached_permissions)

            query = (
                select(PermissionModel.name)
                .join(
                    RolePermissionModel,
                    RolePermissionModel.permission_id == PermissionModel.id,
                )
                .join(
                    UserRoleModel, UserRoleModel.role_id == RolePermissionModel.role_id
                )
                .where(UserRoleModel.user_id == user_id)
            )
            result = await self.postgres_session.execute(query)
            permissions = list(result.scalars().all())

            if permissions:
                await self._set_redis_key(redis_key, permissions)
            return permissions
        except Exception as e:
            self.logger.error(f"Error retrieving permissions for user '{user_id}': {e}")
            raise RepositoryError(
                "Failed to retrieve permissions from the database",
                details=str(e),
                logger=self.logger,
            ) from e

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        redis_key = f"{self.redis_key_prefix}:{user_id}"
        try:
            cached_user = await self._get_redis_key(redis_key)
            if cached_user:
                self.logger.info(f"User '{user_id}' retrieved from Redis.")
                return User.model_validate(json.loads(cached_user))

            result = await self.postgres_session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            user_model = result.scalars().first()
            if user_model:
                user = User.model_validate(user_model)
                await self._set_redis_key(redis_key, user.model_dump())
                return user
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving user by ID '{user_id}': {e}")
            raise RepositoryError(
                "Failed to retrieve user by ID.", str(e), self.logger
            ) from e

    async def get_user(self, username: str) -> User | None:
        redis_key = f"{self.redis_key_prefix}:username:{username}"
        try:
            cached_user = await self._get_redis_key(redis_key)
            if cached_user:
                self.logger.info(f"User '{username}' retrieved from Redis.")
                return User.model_validate(json.loads(cached_user))

            result = await self.postgres_session.execute(
                select(UserModel).where(UserModel.username == username)
            )
            user_model = result.scalars().first()
            if user_model:
                user = User.model_validate(user_model)
                await self._set_redis_key(redis_key, user.model_dump())
                return user
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving user by username '{username}': {e}")
            raise RepositoryError(
                "Failed to retrieve user by username.", str(e), self.logger
            ) from e

    async def save(self, user: User) -> None:
        redis_key = f"{self.redis_key_prefix}:email:{user.email}"
        try:
            user.prepare_for_database()
            user_model = UserModel(**user.model_dump())

            self.postgres_session.add(user_model)
            await self.postgres_session.flush()

            role_query = await self.postgres_session.execute(
                select(RoleModel).where(RoleModel.name == "User")
            )
            role = role_query.scalars().first()
            if not role:
                raise RepositoryError("Default role 'User' not found.")

            user_role_model = UserRoleModel(
                user_id=user_model.id,
                role_id=role.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            self.postgres_session.add(user_role_model)

            await self.postgres_session.commit()

            await self._set_redis_key(redis_key, user.model_dump())
        except Exception as e:
            await self.postgres_session.rollback()
            self.logger.error(f"Error saving user '{user.username}': {e}")
            raise RepositoryError(
                "Failed to save user to the database",
                details=str(e),
                logger=self.logger,
            ) from e
