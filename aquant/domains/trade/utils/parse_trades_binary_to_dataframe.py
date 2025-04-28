import logging

import numpy as np
import pandas as pd

from aquant.domains.trade.entity import Trade

logger = logging.getLogger("TradeService")


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    return pd.DataFrame([t.__dict__ for t in trades])


def ohlcv_to_df(blob: bytes) -> pd.DataFrame:
    dtype = np.dtype(
        [
            ("ticker", "S10"),
            ("timestamp", "<u8"),
            ("open", "f8"),
            ("high", "f8"),
            ("low", "f8"),
            ("close", "f8"),
            ("volume", "f8"),
        ]
    )
    arr = np.frombuffer(blob, dtype=dtype)
    df = pd.DataFrame(arr)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ns")
    tickers = np.char.decode(arr["ticker"], encoding="ascii")
    tickers = np.char.rstrip(tickers, "\x00")
    df["ticker"] = tickers

    return df


def parse_trades_binary_to_dataframe(binary_data: bytes) -> pd.DataFrame:
    """
    Decodes a bytes array contendo N registros sequenciais no formato:
      - 20s   ticker (ASCII padded)
      - 20s   asset  (ASCII padded)
      - 20s   fk_order_id (ASCII padded)
      - Q     event_time (uint64 nanoseconds since epoch)
      - 50s   price_ascii (ASCII padded)
      - d     quantity (float64)
      - 1s    side (ASCII)
      - 1s    tick_direction (ASCII)
      - I     seller_id (uint32)
      - I     buyer_id  (uint32)

    Retorna um DataFrame com colunas:
      ticker, asset, fk_order_id, buyer_id, seller_id,
      price (float), quantity, side, tick_direction, event_time (datetime64[ns]).
    """

    n = len(binary_data)
    logger.info(f"🔹 Received {n} bytes of binary trade-data.")

    dtype = np.dtype(
        [
            ("ticker", "S20"),
            ("asset", "S20"),
            ("fk_order_id", "S20"),
            ("event_time", ">u8"),
            ("price_ascii", "S50"),
            ("quantity", ">f8"),
            ("side", "S1"),
            ("tick_direction", "S1"),
            ("seller_id", ">u4"),
            ("buyer_id", ">u4"),
        ]
    )
    rec_size = dtype.itemsize
    if n % rec_size != 0:
        logger.warning(f"✂️  {n} não é múltiplo de {rec_size}, truncando extras.")
    count = n // rec_size

    arr = np.frombuffer(binary_data, dtype=dtype, count=count)

    arr = arr.astype(arr.dtype.newbyteorder("="))

    df = pd.DataFrame(arr)

    df[["ticker", "asset", "fk_order_id", "price_ascii", "side", "tick_direction"]] = (
        df[
            ["ticker", "asset", "fk_order_id", "price_ascii", "side", "tick_direction"]
        ].applymap(lambda b: b.decode("ascii", errors="ignore"))
    )

    df["ticker"] = df["ticker"].str.rstrip("\x00")
    df["asset"] = df["asset"].str.rstrip("\x00")
    df["fk_order_id"] = df["fk_order_id"].str.rstrip("\x00")
    df["price_ascii"] = df["price_ascii"].str.rstrip("\x00")
    df["side"] = df["side"].str.rstrip("\x00")
    df["tick_direction"] = df["tick_direction"].str.rstrip("\x00")
    df["event_time"] = pd.to_datetime(df["event_time"], unit="ns")
    df["price"] = pd.to_numeric(df["price_ascii"], errors="coerce")

    df = df[
        [
            "ticker",
            "asset",
            "fk_order_id",
            "buyer_id",
            "seller_id",
            "price",
            "quantity",
            "side",
            "tick_direction",
            "event_time",
        ]
    ]

    logger.info(f"✅ Parsed {len(df)} trades into DataFrame.")
    return df
