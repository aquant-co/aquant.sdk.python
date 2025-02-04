from numpy import numpy as np
from pandas import pandas as pd


# -----------------------------------------------------------------------------
# Helper Function: Convert Binary Trade Data to DataFrame
# -----------------------------------------------------------------------------
def parse_trades_binary_to_dataframe(binary_data: bytes) -> pd.DataFrame:
    """
    Parses binary trade data into a pandas DataFrame using NumPy vectorized operations.

    Expected binary format:
      - 4 bytes: Number of trades (big-endian unsigned int)
      - For each trade (42 bytes):
          - 4 bytes: trade_id (big-endian unsigned int)
          - 4 bytes: stock_id (big-endian unsigned int)
          - 8 bytes: price (big-endian float64)
          - 8 bytes: quantity (big-endian float64)
          - 1 byte: side (S1)
          - 1 byte: tick_direction (S1)
          - 8 bytes: event_time (big-endian float64, epoch seconds)
          - 8 bytes: sending_time (big-endian float64, epoch seconds)
    """
    # Check that there is at least a header.
    if len(binary_data) < 4:
        return pd.DataFrame(
            columns=[
                "trade_id",
                "stock_id",
                "price",
                "quantity",
                "side",
                "tick_direction",
                "event_time",
                "sending_time",
            ]
        )

    # Read the number of trades (header)
    num_trades = np.frombuffer(binary_data[:4], dtype=">u4")[0]
    record_size = 42
    expected_length = 4 + num_trades * record_size
    if len(binary_data) < expected_length:
        raise ValueError(
            f"Binary data length mismatch: expected at least {expected_length} bytes, got {len(binary_data)} bytes"
        )

    # Define the numpy dtype matching the record layout.
    dtype = np.dtype(
        [
            ("trade_id", ">u4"),
            ("stock_id", ">u4"),
            ("price", ">f8"),
            ("quantity", ">f8"),
            ("side", "S1"),
            ("tick_direction", "S1"),
            ("event_time", ">f8"),
            ("sending_time", ">f8"),
        ]
    )

    # Parse the records using frombuffer (skip header with offset=4)
    records = np.frombuffer(binary_data, dtype=dtype, offset=4, count=num_trades)

    # Convert structured array to DataFrame.
    df = pd.DataFrame(records)
    # Convert epoch seconds to datetime.
    df["event_time"] = pd.to_datetime(df["event_time"], unit="s")
    df["sending_time"] = pd.to_datetime(df["sending_time"], unit="s")
    # Decode the single-byte fields from bytes to strings.
    df["side"] = df["side"].str.decode("ascii")
    df["tick_direction"] = df["tick_direction"].str.decode("ascii")
    return df
