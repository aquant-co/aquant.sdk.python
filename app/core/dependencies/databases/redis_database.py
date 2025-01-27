from redis.asyncio import Redis

from app.core.database.redis_database import RedisDatabase

# Instância global do RedisDatabase
redis_db = RedisDatabase()


async def get_redis_client() -> Redis:
    """
    Provides a Redis client instance.

    Yields:
        Redis: Redis client instance.
    """
    try:
        client = await redis_db.connect()  # Garante que a conexão está ativa
        yield client
    finally:
        # Não desconecta no provider para manter consistente com o PostgresDatabase
        pass
