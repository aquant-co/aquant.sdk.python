import redis

from aquant.settings import settings


class RedisClient:
    def __init__(
        self,
        redis_url: str = settings.REDIS_URL,
        use_tls: bool = True,
        max_connections: int = 10,
        socket_timeout: float = 0.1,
    ):
        """
        Initialize RedisClient with TLS support.

        :param redis_url: Redis URL connection.
        :param use_tls: Indicates if TLS must have be used for connection.
        """
        self.redis_url = redis_url
        self.use_tls = use_tls
        self.pool = self._create_connection_pool()
        self.client = redis.StrictRedis(
            connection_pool=self.pool, decode_responses=False
        )
        self.pool = redis.ConnectionPool.from_url(
            redis_url,
            connection_class=redis.SSLConnection if use_tls else redis.Connection,
            max_connections=max_connections,
            socket_timeout=socket_timeout,
        )

    def _create_connection_pool(self):
        """
        Creates a Redis ConnectionPool with TLS optional support.
        """
        connection_class = redis.SSLConnection if self.use_tls else redis.Connection
        return redis.ConnectionPool.from_url(
            self.redis_url, connection_class=connection_class
        )

    def get_client(self):
        """
        Returns a Redis client.
        """
        return self.client

    def ping(self):
        """
        Tests Redis connectivity.
        """
        return self.client.ping()


class RedisClientFactory:
    @staticmethod
    def create_client(redis_url: str, use_tls: bool = True) -> RedisClient:
        """
        Creates an RedisClient instance with the given configurations.

        :param redis_url: Redis URL connection.
        :param use_tls: Indicates if TLS must have be used for connection.
        """
        return RedisClient(redis_url=redis_url, use_tls=use_tls)
