from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.databases import get_postgres_db, get_redis_client
from app.core.dependencies.logger import create_logger
from app.domains.user.repositories import UserRepository
from app.domains.user.services import UserService

POSTGRES_DB_DEPENDENCY = Depends(get_postgres_db)
REDIS_CLIENT_DEPENDENCY = Depends(get_redis_client)


def get_user_service(
    postgres_session: AsyncSession = POSTGRES_DB_DEPENDENCY,
    redis_session: Redis = REDIS_CLIENT_DEPENDENCY,
) -> UserService:
    """
    Dependency provider for UserService.
    """
    logger = create_logger("UserService")
    user_repo = UserRepository(postgres_session, redis_session, logger)
    return UserService(logger, user_repo)
