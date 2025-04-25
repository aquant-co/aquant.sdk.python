from enum import Enum


class Actions(Enum):
    GET_TRADES_BY_ASSET = "get_trades_by_asset"
    GET_TRADES_BY_ASSET_AND_TIMERANGE = "get_trades_by_asset_and_timerange"
    GET_TRADES_BY_TICKER = "get_trades_by_ticker"
    GET_TRADES_BY_TICKER_AND_TIMERANGE = "get_trades_by_ticker_and_timerange"
    GET_TRADES_BY_TIMERANGE = "get_trades_by_timerange"
    GET_OPEN_HIGH_LOW_CLOSED_VOLUME_BY_ASSET = (
        "get_open_high_low_closed_volume_by_asset"
    )
    GET_OPEN_HIGH_LOW_CLOSED_VOLUME_BY_ASSET_AND_TIMERANGE = (
        "get_open_high_low_closed_volume_by_asset_and_timerange"
    )
    GET_OPEN_HIGH_LOW_CLOSED_VOLUME_BY_TICKER = (
        "get_open_high_low_closed_volume_by_ticker"
    )
    GET_OPEN_HIGH_LOW_CLOSED_VOLUME_BY_TICKER_AND_TIMERANGE = (
        "get_open_high_low_closed_volume_by_ticker_and_timerange"
    )
    GET_OPEN_HIGH_LOW_CLOSED_VOLUME_BY_TIMERANGE = (
        "get_open_high_low_closed_volume_by_timerange"
    )
    GET_OPEN_HIGH_LOW_CLOSE_VOLUME_BY_TICKER_TIMERANGE_AND_INTERVAL = (
        "get_open_high_low_close_volume_by_ticker_timerange_and_interval"
    )
