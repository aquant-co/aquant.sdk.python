from enum import Enum


class NatsSubjects(Enum):
    MARKETDATA_BOOK_REQUEST = "marketdata.book.request"
    MARKETDATA_BROKER_REQUEST = "marketdata.broker.request"
    MARKETDATA_SECURITY_REQUEST = "marketdata.security.request"
    MARKETDATA_TRADE_REQUEST = "marketdata.trade.request"
