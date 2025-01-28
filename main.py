import time

from aquant_sdk.redis.client import RedisClient
from aquant_sdk.redis.consumer import RedisConsumer
from aquant_sdk.redis.processor import PrintMessageProcessor

redis_client = RedisClient()

processor = PrintMessageProcessor()

consumer = RedisConsumer(redis_client=redis_client, processor=processor)

start_time = time.perf_counter()

result_df = consumer.consume(keys=["VALE3F_Offer"])

end_time = time.perf_counter()

elapsed_time_s = end_time - start_time
elapsed_time_ms = elapsed_time_s * 1000
elapsed_time_us = elapsed_time_ms * 1000

# print(result_df)
print(
    f"\nTempo de execução: {elapsed_time_s:.6f} segundos | {elapsed_time_ms:.3f} ms | {elapsed_time_us:.0f} µs"
)
