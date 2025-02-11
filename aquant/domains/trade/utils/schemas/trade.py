import struct

from aquant.domains.trade.entity import Trade

trade = Trade()
packed_trade = struct.pack(
    "!Q I I I 20s d d c c d d d",  # 74 bytes no total
    trade.id,  # 8 bytes (BIGINT)
    trade.security_id,  # 4 bytes (INT)
    trade.buyer_id,  # 4 bytes (INT)
    trade.seller_id,  # 4 bytes (INT)
    (
        trade.fk_order_id.encode("ascii")[:20] if trade.fk_order_id else b"\x00" * 20
    ),  # 20 bytes (STRING)
    float(trade.price),  # 8 bytes (FLOAT)
    float(trade.quantity),  # 8 bytes (FLOAT)
    trade.side.encode("ascii") if trade.side else b"\x00",  # 1 byte (CHAR)
    (
        trade.tick_direction.encode("ascii") if trade.tick_direction else b"\x00"
    ),  # 1 byte (CHAR)
    trade.event_time.timestamp() if trade.event_time else 0.0,  # 8 bytes (FLOAT)
    (
        trade.event_received_time.timestamp() if trade.event_received_time else 0.0
    ),  # 8 bytes (FLOAT)
    trade.sending_time.timestamp() if trade.sending_time else 0.0,  # 8 bytes (FLOAT)
)
