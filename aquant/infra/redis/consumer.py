from typing import Any

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
        Initialize the Redis consumer.
        """
        self.logger = logger
        self.redis_client = redis_client.get_client()
        self.processor = processor
        self._stop = False

    def get_data(self, keys: list[str]) -> dict[str, list[dict[str, Any]]]:
        """
        Query Redis and return the raw data, decoding JSON using the shared decode_json method.
        """
        data: dict[str, list[dict[str, Any]]] = {}
        try:
            pipe = self.redis_client.pipeline()
            for key in keys:
                pipe.zrange(key, 0, -1)
            raw_results = pipe.execute()

            for key, raw_entries in zip(keys, raw_results, strict=False):
                if raw_entries:
                    data[key] = [self.decode_json(entry) for entry in raw_entries]
        except Exception as e:
            self.logger.error(f"Erro ao buscar dados no Redis: {e}")
        return data

    def stop(self) -> None:
        """Stop message consumption (used only for tests)."""
        self._stop = True
