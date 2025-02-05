import numpy as np
import pandas as pd
import ujson

from aquant.core.logger import Logger
from aquant.domains.marketdata.interface import MarketdataRepositoryInterface
from aquant.domains.marketdata.utils.dictionaries import BookColumnsList
from aquant.infra.redis import BufferedMessageProcessor, RedisClient


class MarketdataRepository(MarketdataRepositoryInterface):
    """
    MarketdataRepository implementation using Redis as a datasource.
    """

    def __init__(
        self,
        logger: Logger,
        redis_client: RedisClient,
        processor: BufferedMessageProcessor,
    ) -> None:
        self.logger = logger
        self.redis_client = redis_client.get_client()
        self.processor = processor
        self._columns = BookColumnsList

    def get_market_data(self, ticker: str) -> pd.DataFrame:
        """
        Fetches Market Data from Redis for a specific ticker.

        Args:
            ticker (str): Ticker to be queried.

        Returns:
            pd.DataFrame: Raw data of the requested ticker.
        """
        try:
            return self.consume_books([ticker])
        except Exception as e:
            self.logger.error(
                f"Error fetching market data for ticker: {ticker}, due to {e}"
            )
            return pd.DataFrame()

    def consume_books(self, keys: list[str]) -> pd.DataFrame:
        """
        Fetches order book data from Redis and returns it as a DataFrame.

        Args:
            keys (list): List of Redis keys.

        Returns:
            pd.DataFrame: Raw data from Redis.
        """
        if not keys:
            return pd.DataFrame(columns=self._columns)

        max_entries = 10000
        key_arr = np.empty(max_entries, dtype=object)
        time_arr = np.empty(max_entries, dtype=object)
        price_arr = np.empty(max_entries, dtype=np.float64)
        qty_arr = np.empty(max_entries, dtype=np.float64)
        brk_id_arr = np.empty(max_entries, dtype=np.int64)
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
                        brk_id_arr.resize(max_entries, refcheck=False)
                        fk_order_id_arr.resize(max_entries, refcheck=False)

                    try:
                        data = ujson.loads(entry.decode("utf-8"))
                        key_arr[idx] = key
                        time_arr[idx] = data["entry_time"]
                        price_arr[idx] = data["price"]
                        qty_arr[idx] = data["quantity"]
                        brk_id_arr[idx] = data["broker_id"]
                        fk_order_id_arr[idx] = data["fk_order_id"]
                        idx += 1
                    except (KeyError, ujson.JSONDecodeError):
                        continue

                    self.processor.process(data)

            except Exception as e:
                self.logger.error(f"Error processing key '{key}': {str(e)}")
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
                "broker_id": brk_id_arr[:idx],
                "fk_order_id": fk_order_id_arr[:idx],
            }
        )
