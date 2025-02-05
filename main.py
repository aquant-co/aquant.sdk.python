# import asyncio
# import struct
# import time
# from datetime import datetime, timedelta

# import pandas as pd
# from nats.aio.client import Client as NATS
# from nats.aio.errors import ErrNoServers, ErrTimeout

# from aquant.core.utils import parse_trades_binary_to_dataframe
# from aquant.settings import settings


# async def test_marketdata_request() -> pd.DataFrame:
#     """
#     Sends a marketdata request over NATS using a binary payload (start and end time)
#     and converts the binary response into a pandas DataFrame.

#     Returns:
#         pd.DataFrame: DataFrame containing trade data.
#     """
#     nc = NATS()

#     options = {
#         "servers": [settings.NATS_URL],
#         "user": settings.AQUANT_NATS_USER,
#         "password": settings.AQUANT_NATS_PASSWORD,
#     }

#     try:
#         await nc.connect(**options)
#     except ErrNoServers as e:
#         print(f"Error connecting to NATS: {e}")
#         return pd.DataFrame()

#     subject = "marketdata.request"

#     start_time_dt = datetime.now() - timedelta(days=30)
#     end_time_dt = datetime.now()

#     payload = struct.pack("!dd", start_time_dt.timestamp(), end_time_dt.timestamp())

#     try:
#         start_perf = time.perf_counter()
#         response = await nc.request(subject, payload, timeout=2)
#         df = parse_trades_binary_to_dataframe(response.data)
#         end_perf = time.perf_counter()
#         elapsed_time_s = end_perf - start_perf
#         elapsed_time_ms = elapsed_time_s * 1000
#         elapsed_time_us = elapsed_time_ms * 1000

#         print(
#             f"\nTempo de execução: {elapsed_time_s:.6f} segundos | {elapsed_time_ms:.3f} ms | {elapsed_time_us:.0f} µs"
#         )
#         return df

#     except ErrTimeout:
#         print("Request timed out.")
#         return pd.DataFrame()
#     except Exception as e:
#         print(f"Error during request: {e}")
#         return pd.DataFrame()
#     finally:
#         await nc.close()


# if __name__ == "__main__":
#     asyncio.run(test_marketdata_request())

import time

from aquant import Aquant
from aquant.settings import settings

aquant = Aquant(redis_url=settings.REDIS_URL)

start_perf = time.perf_counter()
df = aquant.get_order_book(["VALE3F_Bid"])
print(df)
end_perf = time.perf_counter()
elapsed_time_s = end_perf - start_perf
elapsed_time_ms = elapsed_time_s * 1000
elapsed_time_us = elapsed_time_ms * 1000
print(
    f"\nTempo de execução: {elapsed_time_s:.6f} segundos | {elapsed_time_ms:.3f} ms | {elapsed_time_us:.0f} µs"
)
