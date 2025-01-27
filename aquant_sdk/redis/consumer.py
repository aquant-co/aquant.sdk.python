from aquant_sdk.redis.client import RedisClient
from aquant_sdk.redis.processor import MessageProcessor


class RedisConsumer:
    def __init__(
        self, redis_client: RedisClient, stream_key: str, processor: MessageProcessor
    ) -> None:
        self.redis_client = redis_client.get_client()
        self.stream_key = stream_key
        self.processor = processor
        self._stop = False

    def consume(self, stream_keys=None, real_time=False):
        if stream_keys is None:
            stream_keys = self.redis_client.keys(
                pattern="*_Bid"
            ) + self.redis_client.keys(pattern="*_Offer")
            stream_keys = [key.decode() for key in stream_keys]
            if not stream_keys:
                return

        while not self._stop:
            streams = {key: "$" for key in stream_keys}
            messages = self.redis_client.xread(streams, block=3600)
            for stream, entries in messages:
                stream_name = stream.decode()
                for entry_id, entry_data in entries:
                    self.processor.process(
                        {
                            "stream": stream_name,
                            "id": entry_id.decode(),
                            **{k.decode(): v.decode() for k, v in entry_data.items()},
                        }
                    )
                    if not real_time:
                        return

    def stop(self):
        """
        Interrupts the message consuming. used for tests only
        """
        self._stop = True


class RedisConsumerBuilder:
    def __init__(self) -> None:
        self._redis_client = None
        self._stream_key = None
        self._processor = None

    def with_redis_client(self, redis_client: RedisClient):
        self._redis_client = redis_client
        return self

    def with_stream_key(self, stream_key: str):
        self._stream_key = stream_key
        return self

    def with_processor(self, processor: MessageProcessor):
        self._processor = processor
        return self

    def build(self) -> RedisConsumer:
        if not self._redis_client or not self._stream_key or not self._processor:
            raise ValueError("Every components must have been configured before build")
        return RedisConsumer(self._redis_client, self._stream_key, self._processor)
