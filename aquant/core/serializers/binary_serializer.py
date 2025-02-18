import struct
from typing import Any

import orjson

"""
    TODO Generic class, that help us work with encoding and decoding binary data
    Due:
        software development kit is growing and needs to scalate in a 'cleaner way'
"""


class BinarySerializerService:
    """Handles binary serialization and deserialization."""

    @staticmethod
    def encode(payload: dict) -> bytes:
        """serialize a Python dictionary into bytes."""
        json_bytes = orjson.dumps(payload)
        length = len(json_bytes)
        return struct.pack(f"I{length}s", length, json_bytes)

    @staticmethod
    def decode(
        response: bytes, model: type[Any]
    ) -> list[Any]:  # TODO type accordingly our application needs
        """Deserialize a byte message into a list of objects."""
        try:
            decoded_objects = []
            offset = 0
            struct_format = model.get_struct_format()
            struct_size = struct.calcsize(struct_format)

            while offset < len(response):
                unpacked_data = struct.unpack_from(struct_format, response, offset)
                offset += struct_size
                decoded_objects.append(model.from_binary(unpacked_data))

            return decoded_objects
        except Exception as e:
            raise ValueError(f"Error decoding {model.__name__} - Error : {e}") from e
