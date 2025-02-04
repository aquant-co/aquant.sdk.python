import json

import numpy as np
import pandas as pd

from aquant.redis.client import RedisClient
from aquant.redis.processor import BufferedMessageProcessor


class RedisConsumer:
    def __init__(
        self, redis_client: RedisClient, processor: BufferedMessageProcessor
    ) -> None:
        """
        Inicializa o consumidor de mensagens do Redis.

        Args:
            redis_client (RedisClient): Cliente Redis.
            processor (BufferedMessageProcessor): Processador de mensagens.
        """
        self.redis_client = redis_client.get_client()
        self.processor = processor
        self._stop = False
        self._columns = ["key", "entry_time", "price", "quantity"]

    def consume(self, keys):
        """
        Consome mensagens dos conjuntos ordenados no Redis e retorna um DataFrame.

        Args:
            keys (list): Lista de chaves no Redis a serem consumidas.

        Returns:
            pd.DataFrame: DataFrame com os dados processados.
        """
        if not keys:
            return pd.DataFrame(columns=self._columns)

        max_entries = 10000
        key_arr = np.empty(max_entries, dtype=object)
        time_arr = np.empty(max_entries, dtype=object)
        price_arr = np.empty(max_entries, dtype=np.float64)
        qty_arr = np.empty(max_entries, dtype=np.float64)
        brk_arr = np.empty(max_entries, dtype=np.int64)
        fk_order_id_arr = np.empty(max_entries, dtype=object)
        idx = 0

        for key in keys:
            try:
                pipe = self.redis_client.pipeline()
                pipe.zrange(key, 0, -1)
                raw_entries = pipe.execute()[0]

                if not raw_entries:
                    continue

                for entry in raw_entries:
                    if idx >= max_entries:
                        max_entries *= 2
                        key_arr.resize(max_entries, refcheck=False)
                        time_arr.resize(max_entries, refcheck=False)
                        price_arr.resize(max_entries, refcheck=False)
                        qty_arr.resize(max_entries, refcheck=False)
                    try:
                        data = json.loads(entry.decode("utf-8"))
                        key_arr[idx] = key
                        time_arr[idx] = data["entry_time"]
                        price_arr[idx] = data["price"]
                        qty_arr[idx] = data["quantity"]
                        idx += 1
                    except (KeyError, json.JSONDecodeError):
                        continue

                    self.processor.process(data)

            except Exception as e:
                print(f"Erro ao processar chave '{key}': {str(e)}")
                continue

        if idx == 0:
            return pd.DataFrame(columns=self._columns)

        return pd.DataFrame(
            {
                "key": pd.Series(key_arr[:idx], dtype="category"),
                "entry_time": pd.to_datetime(
                    time_arr[:idx], format="%Y%m%d%H%M%S.%f", errors="coerce"
                ),
                "price": price_arr[:idx],
                "quantity": qty_arr[:idx],
                "broker": brk_arr[:idx],
                "fk_order_id": fk_order_id_arr[:idx],
            }
        )

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
