import redis

from aquant.core.logger import Logger


class RedisClient:
    def __init__(
        self,
        logger: Logger,
        redis_url: str,
        use_tls: bool,
        max_connections: int = 10,
        socket_timeout: float = 5.0,
    ):
        self.redis_url = redis_url
        self.logger = logger
        self.use_tls = use_tls
        self.logger.debug(
            f"Inicializando RedisClient com URL: {redis_url} e TLS: {use_tls}"
        )

        self.pool = self._create_connection_pool(max_connections, socket_timeout)
        self.client = redis.StrictRedis(
            connection_pool=self.pool, decode_responses=False
        )
        self.logger.debug("Redis client criado com sucesso.")

    def _create_connection_pool(self, max_connections: int, socket_timeout: float):
        connection_class = redis.SSLConnection if self.use_tls else redis.Connection
        pool = redis.ConnectionPool.from_url(
            self.redis_url,
            connection_class=connection_class,
            max_connections=max_connections,
            socket_timeout=socket_timeout,
        )
        self.logger.debug(
            f"ConnectionPool criado com max_connections={max_connections} e socket_timeout={socket_timeout}"
        )
        return pool

    def get_client(self) -> redis.StrictRedis:
        """
        Retorna o client do Redis.
        """
        self.logger.debug("Obtendo o client Redis.")
        return self.client

    def ping(self):
        """
        Testa a conectividade com o Redis.
        """
        self.logger.debug("Executando ping no Redis.")
        try:
            result = self.client.ping()
            self.logger.debug("Ping realizado com sucesso.")
            return result
        except Exception as e:
            self.logger.error(f"Erro ao executar ping: {e}")
            raise

    def close(self) -> None:
        """
        Fecha a conexão com o Redis.
        """
        self.logger.debug("Fechando conexão com o Redis.")
        try:
            result = self.client.close()
            self.logger.debug("Conexão fechada com sucesso.")
            return result
        except Exception as e:
            self.logger.error(f"Erro ao fechar a conexão: {e}")
            raise
