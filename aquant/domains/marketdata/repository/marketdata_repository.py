from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import orjson as json_lib
import pandas as pd

from aquant.core.logger import Logger
from aquant.core.utils import weak_lru
from aquant.domains.marketdata.utils.dictionaries import BookColumnsList
from aquant.infra.redis import BufferedMessageProcessor, RedisClient


class MarketdataRepository:
    def __init__(
        self,
        logger: Logger,
        redis_client: RedisClient,
        processor: BufferedMessageProcessor,
        max_entries: int = 50000,
        max_workers: int = 4,
    ) -> None:
        self.logger = logger
        self.redis_client = redis_client.get_client()
        self.processor = processor
        self._columns: list[str] = BookColumnsList
        self.max_entries = max_entries
        self.max_workers = max_workers

    @staticmethod
    def decode_json(b: bytes) -> Any:
        """Decode bytes into a Python object using orjson."""
        return json_lib.loads(b)

    def _process_key_entries(
        self, key: str, raw_entries: list[bytes], max_entries: int
    ) -> dict[str, list[Any]]:
        """
        Process entries for a single Redis key.
        Decodes and extracts fields in one pass.
        """
        entries: dict[str, list[Any]] = {
            "key": [],
            "entry_time": [],
            "price": [],
            "quantity": [],
            "broker_id": [],
            "fk_order_id": [],
        }
        for entry_bytes in raw_entries[:max_entries]:
            try:
                entry = self.decode_json(entry_bytes)
                self.processor.process(entry)
                entries["key"].append(key)
                entries["entry_time"].append(entry.get("entry_time"))
                entries["price"].append(entry.get("price"))
                entries["quantity"].append(entry.get("quantity"))
                entries["broker_id"].append(entry.get("broker_id"))
                entries["fk_order_id"].append(entry.get("fk_order_id"))
            except Exception as e:
                self.logger.warning(f"Skipping invalid entry for {key}: {e}")
        return entries

    @weak_lru(maxsize=128)
    def get_current_book_cached(self, ticker_tuple: tuple[str, ...]) -> pd.DataFrame:
        """Cache recent queries. Convert the ticker list to a tuple for hashability."""
        return self.get_current_book(list(ticker_tuple))

    def get_current_book(
        self,
        tickers: list[str],
        side: list[str] | None = None,
        max_age_minutes: int = 5,
        only_recent: bool = False,
    ) -> pd.DataFrame:
        """
        Fetch order book data from Redis for the provided tickers and return a DataFrame.
        If only_recent is True, filter rows based on the entry_time column.
        """
        if only_recent:
            current_time = pd.Timestamp.now()
            df = super().get_current_book(tickers)
            return df[
                df["entry_time"]
                > (current_time - pd.Timedelta(minutes=max_age_minutes))
            ]
        if not tickers:
            return pd.DataFrame(columns=self._columns)

        pipe = self.redis_client.pipeline()
        for key in tickers:
            pipe.zrange(key, 0, self.max_entries - 1)
        raw_results = pipe.execute()

        all_entries: dict[str, list[Any]] = {col: [] for col in self._columns}
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_key = {
                executor.submit(
                    self._process_key_entries, key, raw, self.max_entries
                ): key
                for key, raw in zip(tickers, raw_results, strict=False)
            }
            for future in as_completed(future_to_key):
                try:
                    key_entries = future.result()
                    for col in all_entries:
                        all_entries[col].extend(key_entries[col])
                except Exception as e:
                    self.logger.error(
                        f"Error processing key {future_to_key[future]}: {e}"
                    )

        if not all_entries["key"]:
            return pd.DataFrame(columns=self._columns)

        df = pd.DataFrame(
            {
                "key": pd.Series(all_entries["key"], dtype="category"),
                "entry_time": pd.to_datetime(
                    all_entries["entry_time"], format="%Y%m%d%H%M%S.%f", errors="coerce"
                ),
                "price": all_entries["price"],
                "quantity": all_entries["quantity"],
                "broker_id": all_entries["broker_id"],
                "fk_order_id": all_entries["fk_order_id"],
            }
        )

        return df
