import logging

import numpy as np
import pandas as pd

logger = logging.getLogger("TradeService")


# -----------------------------------------------------------------------------
# Helper Function: Convert Binary Trade Data to DataFrame
# -----------------------------------------------------------------------------
def parse_trades_binary_to_dataframe(binary_data: bytes) -> pd.DataFrame:
    """
    Converts binary data from md_security_movement into a pandas DataFrame.
    """
    logger.info(f"🔹 Received {len(binary_data)} bytes of binary data.")

    if len(binary_data) < 4:
        logger.warning(
            "⚠️ Binary data too small to contain header. Returning empty DataFrame."
        )
        return pd.DataFrame(
            columns=[
                "security_id",
                "ticker",
                "buyer_id",
                "seller_id",
                "fk_order_id",
                "price",
                "quantity",
                "side",
                "tick_direction",
                "event_time",
            ]
        )

    num_records_header = int.from_bytes(binary_data[:4], byteorder="big")

    dtype = np.dtype(
        [
            ("security_id", ">u4"),
            ("ticker", "S20"),
            ("buyer_id", ">u4"),
            ("seller_id", ">u4"),
            ("fk_order_id", "S20"),
            ("price", ">f8"),
            ("quantity", ">f8"),
            ("side", "S1"),
            ("tick_direction", "S1"),
            ("event_time", ">u8"),
        ]
    )
    record_size = dtype.itemsize
    num_records_actual = (len(binary_data) - 4) // record_size
    num_records = min(num_records_header, num_records_actual)
    expected_length = 4 + num_records * record_size

    if len(binary_data) < expected_length:
        logger.error(
            f"Binary data size mismatch! Expected {expected_length} bytes, got {len(binary_data)} bytes."
        )
        raise ValueError("Binary data size does not match expected size.")

    try:
        records = np.frombuffer(binary_data, dtype=dtype, offset=4, count=num_records)
    except ValueError as e:
        logger.error(f"Error parsing binary data: {e}.")
        raise

    records = records.astype(records.dtype.newbyteorder("="))

    logger.info(
        f"Successfully parsed {num_records} records into a structured NumPy array."
    )

    df = pd.DataFrame(records)

    df["event_time"] = pd.to_datetime(df["event_time"], unit="ns", errors="coerce")

    df["side"] = df["side"].str.decode("ascii", errors="ignore")
    df["tick_direction"] = df["tick_direction"].str.decode("ascii", errors="ignore")
    df["fk_order_id"] = df["fk_order_id"].str.decode("ascii", errors="ignore")

    logger.info(f"Converted binary data to DataFrame with {df.shape[0]} rows.")
    return df
