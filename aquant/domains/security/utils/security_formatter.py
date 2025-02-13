import struct
from datetime import datetime

import orjson

from aquant.domains.security.entity import Security


def encode_security(payload: dict) -> bytes:
    """Serialize a Python dictionary into bytes"""
    json_str = orjson.dumps(payload)
    json_bytes = json_str
    length = len(json_bytes)

    return struct.pack(f"I{length}s", length, json_bytes)


def decode_securities(response: bytes) -> list[Security]:
    """Deserialize byte message into a Security dict"""
    try:
        securities = []
        offset = 0
        struct_format = "!50s13s50s50sI I 50s50s50sI3s I I I I f I 50s I I"
        struct_size = struct.calcsize(struct_format)

        while offset < len(response):
            unpacked_data = struct.unpack_from(struct_format, response, offset)
            offset += struct_size

            def safe_decode(data):
                if isinstance(data, bytes):
                    return data.decode("utf-8").strip("\x00")
                return None

            security = Security(
                asset=safe_decode(unpacked_data[0]),
                ticker=safe_decode(unpacked_data[1]),
                isin=safe_decode(unpacked_data[2]),
                cfi_code=safe_decode(unpacked_data[3]),
                product=unpacked_data[4] if unpacked_data[4] != 0 else None,
                type=unpacked_data[5] if unpacked_data[5] != 0 else None,
                sub_type=safe_decode(unpacked_data[6]),
                name=safe_decode(unpacked_data[7]),
                security_group=safe_decode(unpacked_data[8]),
                price_type=unpacked_data[9],
                currency=safe_decode(unpacked_data[10]),
                round_lot=unpacked_data[11] if unpacked_data[11] != 0 else None,
                tick_size_denominator=(
                    unpacked_data[12] if unpacked_data[12] != 0 else None
                ),
                min_order_quantity=(
                    unpacked_data[13] if unpacked_data[13] != 0 else None
                ),
                max_order_quantity=(
                    unpacked_data[14] if unpacked_data[14] != 0 else None
                ),
                min_price_increment=(
                    unpacked_data[15] if unpacked_data[15] != 0.0 else None
                ),
                issued_at=(
                    datetime.fromtimestamp(unpacked_data[16])
                    if unpacked_data[16] != 0
                    else None
                ),
                issued_at_country=safe_decode(unpacked_data[17]),
                expires_at=(
                    datetime.fromtimestamp(unpacked_data[18])
                    if unpacked_data[18] != 0
                    else None
                ),
                expired_at=(
                    datetime.fromtimestamp(unpacked_data[19])
                    if unpacked_data[19] != 0
                    else None
                ),
            )

            securities.append(security)

        return securities
    except Exception as e:
        raise ValueError(f"Error at decoding_securities, due: {e}") from e
