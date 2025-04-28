import logging

import numpy as np
import pandas as pd

logger = logging.getLogger("TradeService")


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
    logger.debug(f"Received {n} bytes of binary trade-data.")

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
        logger.warning(f"{n} bytes não é múltiplo de {rec_size}, truncando extras.")
    count = n // rec_size

    arr = np.frombuffer(binary_data, dtype=dtype, count=count)
    arr = arr.astype(arr.dtype.newbyteorder("="))

    tickers = np.char.decode(arr["ticker"], "ascii")
    tickers = np.char.rstrip(tickers, "\x00")
    assets = np.char.decode(arr["asset"], "ascii")
    assets = np.char.rstrip(assets, "\x00")
    fk_ids = np.char.decode(arr["fk_order_id"], "ascii")
    fk_ids = np.char.rstrip(fk_ids, "\x00")
    prices_ascii = np.char.decode(arr["price_ascii"], "ascii")
    prices_ascii = np.char.rstrip(prices_ascii, "\x00")
    sides = np.char.decode(arr["side"], "ascii")
    tdirs = np.char.decode(arr["tick_direction"], "ascii")

    df = pd.DataFrame(
        {
            "ticker": tickers,
            "asset": assets,
            "fk_order_id": fk_ids,
            "buyer_id": arr["buyer_id"],
            "seller_id": arr["seller_id"],
            "price": pd.to_numeric(prices_ascii, errors="coerce"),
            "quantity": arr["quantity"],
            "side": sides,
            "tick_direction": tdirs,
            "event_time": pd.to_datetime(arr["event_time"], unit="ns"),
        }
    )

    logger.debug(f"Parsed {len(df)} trades into DataFrame.")
    return df
