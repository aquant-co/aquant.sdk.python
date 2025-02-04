# """
# Example how to use this SDK:
# Just import thoese

# Preço, volume, abertura e fechamento, informações do ativo, etc...

# """

# import asyncio
# import json
# import time

# from nats.aio.client import Client as NATS
# from nats.aio.errors import ErrTimeout

# from aquant_sdk.redis.client import RedisClient
# from aquant_sdk.redis.consumer import RedisConsumer
# from aquant_sdk.redis.processor import BufferedMessageProcessor

# redis_client = RedisClient()

# processor = BufferedMessageProcessor()

# consumer = RedisConsumer(redis_client=redis_client, processor=processor)

# start_time = time.perf_counter()

# result_df = consumer.consume(keys=["VALE3F_Offer"])

# end_time = time.perf_counter()

# elapsed_time_s = end_time - start_time
# elapsed_time_ms = elapsed_time_s * 1000
# elapsed_time_us = elapsed_time_ms * 1000

# print(result_df)
# print(
#     f"\nTempo de execução: {elapsed_time_s:.6f} segundos | {elapsed_time_ms:.3f} ms | {elapsed_time_us:.0f} µs"
# )

import asyncio
import struct
import time
from datetime import datetime, timedelta

import pandas as pd
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrNoServers, ErrTimeout

from aquant_sdk.core.utils import parse_trades_binary_to_dataframe
from aquant_sdk.settings import settings


# -----------------------------------------------------------------------------
# SDK Method: test_marketdata_request
# -----------------------------------------------------------------------------
async def test_marketdata_request() -> pd.DataFrame:
    """
    Sends a marketdata request over NATS using a binary payload (start and end time)
    and converts the binary response into a pandas DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing trade data.
    """
    nc = NATS()

    options = {
        "servers": [settings.NATS_URL],
        "user": settings.AQUANT_NATS_USER,
        "password": settings.AQAUNT_NATS_PASSWORD,
    }

    try:
        await nc.connect(**options)
    except ErrNoServers as e:
        print(f"Error connecting to NATS: {e}")
        return pd.DataFrame()

    subject = "marketdata.request"

    start_time_dt = datetime.now() - timedelta(days=30)
    end_time_dt = datetime.now()

    payload = struct.pack("!dd", start_time_dt.timestamp(), end_time_dt.timestamp())

    try:
        start_perf = time.perf_counter()
        response = await nc.request(subject, payload, timeout=2)
        df = parse_trades_binary_to_dataframe(response.data)
        end_perf = time.perf_counter()
        elapsed_time_s = end_perf - start_perf
        elapsed_time_ms = elapsed_time_s * 1000
        elapsed_time_us = elapsed_time_ms * 1000

        # print(df)
        print(
            f"\nTempo de execução: {elapsed_time_s:.6f} segundos | {elapsed_time_ms:.3f} ms | {elapsed_time_us:.0f} µs"
        )
        return df

    except ErrTimeout:
        print("Request timed out.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error during request: {e}")
        return pd.DataFrame()
    finally:
        await nc.close()


# -----------------------------------------------------------------------------
# Example usage (if running the SDK method directly)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(test_marketdata_request())
