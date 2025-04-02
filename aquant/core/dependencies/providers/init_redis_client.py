from aquant.core.logger import Logger
from aquant.infra.redis import RedisClient


async def init_redis_client(redis_url: str, logger: Logger, use_tls: bool = True):
    """
    Cria uma instância de RedisClient com as configurações fornecidas.

    :param redis_url: URL de conexão com o Redis.
    :param logger: Instância de Logger para registro.
    :param use_tls: Define se TLS deve ser utilizado.
    """
    redis_client = RedisClient(redis_url=redis_url, logger=logger, use_tls=use_tls)

    yield redis_client
    redis_client.close()
