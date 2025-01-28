import redis

from aquant_sdk.settings import settings


class RedisClient:
    def __init__(self, redis_url: str = settings.REDIS_URL, use_tls: bool = True):
        """
        Inicializa o RedisClient com suporte a TLS.

        :param redis_url: URL de conexão do Redis.
        :param use_tls: Indica se TLS deve ser usado para a conexão.
        """
        self.redis_url = redis_url
        self.use_tls = use_tls
        self.pool = self._create_connection_pool()
        self.client = redis.StrictRedis(
            connection_pool=self.pool, decode_responses=False
        )

    def _create_connection_pool(self):
        """
        Cria uma ConnectionPool para o Redis com suporte opcional a TLS.
        """
        connection_class = redis.SSLConnection if self.use_tls else redis.Connection
        return redis.ConnectionPool.from_url(
            self.redis_url, connection_class=connection_class
        )

    def get_client(self):
        """
        Retorna o cliente Redis.
        """
        return self.client

    def ping(self):
        """
        Testa a conectividade com o Redis.
        """
        return self.client.ping()


class RedisClientFactory:
    @staticmethod
    def create_client(redis_url: str, use_tls: bool = True) -> RedisClient:
        """
        Cria uma instância de RedisClient com as configurações fornecidas.

        :param redis_url: URL de conexão do Redis.
        :param use_tls: Indica se TLS deve ser usado para a conexão.
        """
        return RedisClient(redis_url=redis_url, use_tls=use_tls)
