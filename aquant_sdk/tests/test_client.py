from aquant_sdk.redis import RedisClient, RedisClientFactory
from aquant_sdk.settings import settings


def test_redis_client_initialization():
    redis_client = RedisClient(redis_url=settings.REDIS_URL, use_tls=True)
    assert redis_client.ping()


def test_redis_client_factory():
    redis_client = RedisClientFactory.create_client(
        redis_url=settings.REDIS_URL, use_tls=True
    )
    assert redis_client.ping()
