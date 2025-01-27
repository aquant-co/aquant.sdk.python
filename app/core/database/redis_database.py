from redis.asyncio import Redis

from app.core.config.settings import Settings
from app.core.database.database_interface import DatabaseInterface


class RedisDatabase(DatabaseInterface):
    """
    Redis implementation for connection management and client retrieval.

    Attributes:
        redis_url (str): URL for connecting to the Redis instance.
        session (Redis): Redis client instance.
    """

    def __init__(self, redis_url: str = None):
        settings = Settings()
        self.redis_url = redis_url or settings.REDIS_URL
        self.session: Redis = None

    async def connect(self) -> Redis:
        """
        Ensures the Redis client is connected and returns it.

        Returns:
            Redis: Redis client instance.
        """
        if not self.session:
            self.session = Redis.from_url(self.redis_url, decode_responses=True)
            try:
                await self.session.ping()  # Test connection
                print("Redis connection established.")
            except Exception as e:
                raise RuntimeError(f"Failed to connect to Redis: {e}") from e
        return self.session

    async def disconnect(self) -> None:
        """
        Closes the Redis connection and releases resources.
        """
        if self.session:
            await self.session.close()
            self.session = None
            print("Redis connection closed.")

    def get_client(self) -> Redis:
        """
        Returns the Redis client.

        Returns:
            Redis: Redis client instance.
        """
        if not self.session:
            raise RuntimeError("Redis client is not initialized. Call connect() first.")
        return self.session
