import struct
from datetime import datetime
from decimal import Decimal

import pandas as pd

from aquant.core.logger import Logger
from aquant.core.serializers import BinarySerializerService
from aquant.domains.trade.dtos import TradeDTO
from aquant.domains.trade.entity import Trade


class TradeParserService:
    def __init__(self, logger=Logger) -> None:
        self.logger = logger

    @staticmethod
    def safe_decode(data: bytes) -> str | None:
        """Decodes bytes safely, stripping null bytes."""
        return data.decode("utf-8").strip("\x00") if isinstance(data, bytes) else None

    def encode_trades(self, message: TradeDTO) -> bytes:
        try:
            self.logger.info("Trying to serialize trade payload data into binary...")

            return BinarySerializerService.encode(message.model_dump())
        except Exception as e:
            self.logger.error(
                "Error trying to encode trade payload data into binary before sending to Nats"
            )
            raise RuntimeError(
                f"Unexpected error has occured while trying encode trade payload data into binary before sending to Nats, error: {e}"
            ) from e

    def decode(self, message: bytes) -> list[Trade]:
        """
        Decodes a binary trade message into a TradeDTO object.
        """
        try:
            decoded_data = BinarySerializerService.decode(message, Trade)

            if not decoded_data:
                raise ValueError("Decoded trade message is empty")
            return decoded_data

        except ValueError as ve:
            self.logger.error(f"ValueError decoding message: {ve}")
            raise ve

        except Exception as e:
            self.logger.error(f"Unexpected error decoding message: {e}")
            raise RuntimeError(f"Unknown error decoding message: {e}") from e

    def decode_trades(self, binary_data: bytes) -> list[Trade]:
        """
        Decodes binary trade data into a list of `Trade` objects.
        """
        try:
            trades = []
            offset = 0

            struct_format = "!20s 20s 20s Q 50s d 1s 1s I I"
            struct_size = struct.calcsize(struct_format)

            if len(binary_data) < struct_size:
                self.logger.warning("Binary data too small, returning empty list.")
                return []

            while offset + struct_size <= len(binary_data):
                unpacked_data = struct.unpack_from(struct_format, binary_data, offset)
                offset += struct_size

                trade = Trade(
                    ticker=self.safe_decode(unpacked_data[0]),
                    asset=self.safe_decode(unpacked_data[1]),
                    fk_order_id=self.safe_decode(unpacked_data[2]),
                    event_time=(
                        datetime.utcfromtimestamp(unpacked_data[3] / 1e9)
                        if unpacked_data[3] != 0
                        else None
                    ),
                    price=Decimal(self.safe_decode(unpacked_data[4]).strip() or "0"),
                    quantity=(
                        Decimal(unpacked_data[5])
                        if unpacked_data[5] > 0
                        else Decimal(0)
                    ),
                    side=self.safe_decode(unpacked_data[6]) or "B",
                    tick_direction=self.safe_decode(unpacked_data[7]) or "=",
                    seller_id=unpacked_data[8],
                    buyer_id=unpacked_data[9],
                )

                trades.append(trade)

            self.logger.info(f"Successfully decoded {len(trades)} trade records.")
            return trades

        except struct.error as e:
            self.logger.error(f"Struct unpack error: {e}")
            raise ValueError(f"Error decoding trades: {e}") from e

        except Exception as e:
            self.logger.error(f"Unexpected error decoding trades: {e}")
            raise ValueError(f"Unknown error decoding trades: {e}") from e

    def parse_trades_to_dataframe(self, binary_data: bytes) -> pd.DataFrame:
        """
        Converts binary trade data into a pandas DataFrame.
        """
        try:
            trades = self.decode_trades(binary_data)
            if not trades:
                return pd.DataFrame(
                    columns=[field for field in Trade.model_fields.keys()]
                )

            df = pd.DataFrame([trade.model_dump() for trade in trades])

            self.logger.info(
                f"Converted binary data to DataFrame with {df.shape[0]} rows."
            )
            return df
        except Exception as e:
            self.logger.error(f"Error parsing trades into DataFrame: {e}")
            raise e
