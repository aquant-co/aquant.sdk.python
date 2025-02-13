def parse_brokers_binary_to_string(binary_data: bytes) -> str:
    """
    Parses a fixed-length binary message containing the broker's name.

    Expected format:
      - 64 bytes: Broker name, encoded in UTF-8 and padded with null bytes.

    Returns:
      The broker name as a Python string.
    """
    fixed_length = 64
    if len(binary_data) != fixed_length:
        raise ValueError(
            f"Expected {fixed_length} bytes, but got {len(binary_data)} bytes"
        )

    broker_name = binary_data.rstrip(b"\x00").decode("utf-8")
    return broker_name
