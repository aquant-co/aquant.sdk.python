import json

import pandas as pd

from aquant_sdk.redis.client import RedisClient
from aquant_sdk.redis.processor import MessageProcessor


class RedisConsumer:
    def __init__(self, redis_client: RedisClient, processor: MessageProcessor) -> None:
        """
        Inicializa o consumidor de mensagens do Redis.

        Args:
            redis_client (RedisClient): Cliente Redis.
            processor (MessageProcessor): Processador de mensagens.
        """
        self.redis_client = redis_client.get_client()
        self.processor = processor
        self._stop = False

    def consume(self, keys):
        """
        Consome dados dos Sorted Sets no Redis com base nas chaves fornecidas.

        Args:
            keys (list[str]): Lista de chaves a serem consultadas.

        Returns:
            pd.DataFrame: DataFrame com os dados coletados.
        """
        if not keys:
            print("Nenhuma chave fornecida para consumo. Retornando vazio.")
            return pd.DataFrame(columns=["key", "entry_time", "price", "quantity"])

        results = []

        try:
            for key in keys:
                print(f"Lendo dados da chave: {key}")

                raw_entries = self.redis_client.zrange(key, 0, -1)

                if not raw_entries:
                    print(f"Nenhum dado encontrado para {key}")
                    continue

                for entry in raw_entries:
                    try:
                        entry_data = json.loads(entry.decode())
                        entry_data["key"] = key
                        results.append(entry_data)
                        self.processor.process(entry_data)
                    except json.JSONDecodeError:
                        print(f"Erro ao decodificar JSON da chave: {key}")

            print("Processamento sob demanda concluído.")
            return (
                pd.DataFrame(results)
                if results
                else pd.DataFrame(columns=["key", "entry_time", "price", "quantity"])
            )

        except Exception as e:
            print(f"Erro durante o consumo de mensagens: {e}")
            return pd.DataFrame(columns=["key", "entry_time", "price", "quantity"])

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

    def with_processor(self, processor: MessageProcessor):
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
