import json

from aquant.core.logger import Logger
from aquant.infra.redis.client import RedisClient
from aquant.infra.redis.processor import BufferedMessageProcessor


class RedisConsumer:
    def __init__(
        self,
        logger: Logger,
        redis_client: RedisClient,
        processor: BufferedMessageProcessor,
    ) -> None:
        """
        Inicializa o consumidor de mensagens do Redis.

        Args:
            redis_client (RedisClient): Cliente Redis.
            processor (BufferedMessageProcessor): Processador de mensagens.
        """
        self.logger = logger
        self.redis_client = redis_client.get_client()
        self.processor = processor
        self._stop = False
        self._columns = ["key", "entry_time", "price", "quantity"]

    def get_data(self, keys: list[str]) -> dict[str, list[dict[str, any]]]:
        """
        Consulta o Redis e retorna os dados brutos.

        Args:
            keys (list): Lista de chaves no Redis.

        Returns:
            dict: Dicionário com os dados organizados por chave.
        """
        data = {}
        try:
            pipe = self.redis_client.pipeline()
            for key in keys:
                pipe.zrange(key, 0, -1)
            raw_results = pipe.execute()

            for key, raw_entries in zip(keys, raw_results, strict=False):
                if raw_entries:
                    data[key] = [
                        json.loads(entry.decode("utf-8")) for entry in raw_entries
                    ]
        except Exception as e:
            self.logger.error(f"Erro ao buscar dados no Redis: {e}")

        return data

    def stop(self):
        """
        Interrompe o consumo de mensagens (usado apenas para testes).
        """
        self._stop = True


class RedisConsumerBuilder:
    def __init__(self) -> None:
        """
        Builder para a criação de RedisConsumer de forma modular.
        """
        self._redis_client = None
        self._processor = None

    def with_redis_client(self, redis_client: RedisClient):
        self._redis_client = redis_client
        return self

    def with_processor(self, processor: BufferedMessageProcessor):
        self._processor = processor
        return self

    def build(self) -> RedisConsumer:
        """
        Constrói uma instância de RedisConsumer.

        Returns:
            RedisConsumer: Instância configurada de RedisConsumer.
        """
        if not self._redis_client or not self._processor:
            raise ValueError(
                "Redis client e processor devem ser configurados antes de construir."
            )
        return RedisConsumer(self._redis_client, self._processor)
