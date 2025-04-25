from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import orjson as json_lib
import pandas as pd

from aquant.core.logger import Logger
from aquant.core.utils import weak_lru
from aquant.domains.marketdata.utils.dictionaries import BookColumnsList
from aquant.domains.marketdata.utils.redis import generate_redis_keys
from aquant.infra.redis import BufferedMessageProcessor, RedisClient


class MarketdataRepository:
    def __init__(
        self,
        logger: Logger,
        redis_client: RedisClient,
        processor: BufferedMessageProcessor,
        max_workers: int = 4,
    ) -> None:
        self.logger = logger
        self.redis_client = redis_client.get_client()
        self.processor = processor
        self._columns: list[str] = BookColumnsList
        self.max_workers = max_workers

    @staticmethod
    def decode_json(b: bytes) -> Any:
        """Decode bytes into a Python object using orjson."""
        return json_lib.loads(b)

    def _process_key_entries(
        self, key: str, entries_list: list[dict[str, Any]], max_entries: int
    ) -> dict[str, list[Any]]:
        cols = {
            "key": [],
            "entry_time": [],
            "price": [],
            "quantity": [],
            "broker_id": [],
            "fk_order_id": [],
        }

        for entry in entries_list[:max_entries]:
            try:
                date_str = entry["entry_date"]
                t_int = entry["entry_time"]
                s = f"{t_int:09d}"
                hh, mm, ss, ms = (int(s[0:2]), int(s[2:4]), int(s[4:6]), int(s[6:]))
                ts = pd.Timestamp(
                    year=int(date_str[0:4]),
                    month=int(date_str[4:6]),
                    day=int(date_str[6:8]),
                    hour=hh,
                    minute=mm,
                    second=ss,
                    microsecond=ms * 1_000,
                )

                self.processor.process(entry)

                cols["key"].append(key)
                cols["entry_time"].append(ts)
                cols["price"].append(entry["price"])
                cols["quantity"].append(entry["quantity"])
                cols["broker_id"].append(entry["broker_id"])
                cols["fk_order_id"].append(entry["fk_order_id"])

            except Exception as e:
                self.logger.warning(f"Skipping invalid entry for {key}: {e}")

        return cols

    @weak_lru(maxsize=128)
    def get_current_book_cached(self, ticker_tuple: tuple[str, ...]) -> pd.DataFrame:
        return self.get_current_book(list(ticker_tuple))

    def get_current_book(
        self,
        tickers: list[str],
        max_entries: int,
        side: list[str] | None = None,
        max_age_minutes: int = 5,
        only_recent: bool = False,
    ) -> pd.DataFrame:
        if only_recent:
            current_time = pd.Timestamp.now()
            df = super().get_current_book(tickers)
            return df[
                df["entry_time"]
                > (current_time - pd.Timedelta(minutes=max_age_minutes))
            ]

        if not tickers:
            return pd.DataFrame(columns=self._columns)

        keys = (
            generate_redis_keys(tickers)
            if side is None
            else [f"aquant.security,{t}.book.{s}" for t in tickers for s in side]
        )

        pipe = self.redis_client.pipeline()
        for key in keys:
            pipe.get(key)
        raw_results = pipe.execute()

        decoded_lists: list[list[dict[str, Any]]] = []
        for key, raw in zip(keys, raw_results, strict=False):
            if raw:
                try:
                    arr = json_lib.loads(raw)
                    if isinstance(arr, dict):
                        arr = [arr]
                except Exception as e:
                    self.logger.warning(f"Invalid JSON for {key}: {e}")
                    arr = []
            else:
                arr = []
            decoded_lists.append(arr)

        all_entries: dict[str, list[Any]] = {c: [] for c in self._columns}
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_key = {
                executor.submit(
                    self._process_key_entries, key, entries_list, max_entries
                ): key
                for key, entries_list in zip(keys, decoded_lists, strict=False)
            }
            for future in as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    cols = future.result()
                    for col, vals in cols.items():
                        all_entries[col].extend(vals)
                except Exception as e:
                    self.logger.error(f"Error processing key {key}: {e}")

        if not all_entries["key"]:
            return pd.DataFrame(columns=self._columns)

        df = pd.DataFrame(
            {
                "key": pd.Series(all_entries["key"], dtype="category"),
                "entry_time": all_entries["entry_time"],
                "price": all_entries["price"],
                "quantity": all_entries["quantity"],
                "broker_id": all_entries["broker_id"],
                "fk_order_id": all_entries["fk_order_id"],
            }
        )

        self.processor.flush()

        return df
