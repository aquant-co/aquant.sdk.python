import orjson

from aquant.domains.trade.entity import Trade


class TradeJSONCodec:
    """Codec for encoding/decoding Trade Objects to/from JSON format."""

    __slots__ = ()  # no instance attributes (stateless)

    def encode(self, trade: Trade) -> bytes:
        """
        Convert a Trade object to a JSON byte string.
        Using orjson for High performance serialization
        """
        try:
            # Use orjson's dataclass support for direct serialization
            json_bytes: bytes = orjson.dumps(
                trade, option=orjson.OPT_SERIALIZE_DATACLASS
            )
        except Exception:
            """
            In an HFT context, this should rarely fail if types are correct.
            We handle any exception minimally (could log error and rethrow or return None).
            Keeping error handling minimal for performance.
            """
            raise
        return json_bytes

    def decode(self, data: bytes) -> Trade:
        """
        Parse a JSON byte string (or str) to a trade object.
        Expects data to be a valid JSON representing a trade
        """

        try:
            obj = orjson.loads(data)
        except Exception:
            raise
        return Trade(**obj)
