from datetime import datetime

from aquant.core.logger import Logger
from aquant.domains.trade.dtos import TradeDTO, TradeParamsDTO
from aquant.domains.trade.utils.enums import Actions, TimescaleIntervalEnum


class TradePayloadBuilderService:
    """
    Service responsible for building trade request payloads.
    """

    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    ACTIONS_MAP = {
        ("ticker", "timerange"): Actions.GET_TRADES_BY_TICKER_AND_TIMERANGE.value,
        ("asset", "timerange"): Actions.GET_TRADES_BY_ASSET_AND_TIMERANGE.value,
        ("timerange",): Actions.GET_TRADES_BY_TIMERANGE.value,
        ("ticker",): Actions.GET_TRADES_BY_TICKER.value,
        ("asset",): Actions.GET_TRADES_BY_ASSET.value,
    }

    ACTIONS_OHLCV_MAP = {
        (
            "ticker",
            "timerange",
        ): Actions.GET_OPEN_HIGH_LOW_CLOSED_VOLUME_BY_TICKER_AND_TIMERANGE.value,
        (
            "ticker",
            "interval",
            "start_time",
            "end_time",
        ): Actions.GET_OPEN_HIGH_LOW_CLOSE_VOLUME_BY_TICKER_TIMERANGE_AND_INTERVAL.value,
        (
            "asset",
            "timerange",
        ): Actions.GET_OPEN_HIGH_LOW_CLOSED_VOLUME_BY_ASSET_AND_TIMERANGE.value,
        ("timerange",): Actions.GET_OPEN_HIGH_LOW_CLOSED_VOLUME_BY_TIMERANGE.value,
        ("ticker",): Actions.GET_OPEN_HIGH_LOW_CLOSED_VOLUME_BY_TICKER.value,
        ("asset",): Actions.GET_OPEN_HIGH_LOW_CLOSED_VOLUME_BY_ASSET.value,
    }

    def trade_payload_builder(
        self,
        ticker: str | None = None,
        asset: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        ohlcv: bool = False,
    ) -> TradeDTO:
        """
        Builds a TradeDTO for trade requests, binding the correct action based on provided parameters.

        Args:
            ticker (Optional[str]): Active code.
            asset (Optional[str]): Active name.
            start_time (Optional[datetime]): Start time of the query.
            end_time (Optional[datetime]): End time of the query.
            ohlcv (bool): If 'True', returns Open-High-Low-Close-Volume (OHLCV).

        Returns:
            TradeDTO: DTO containing action and parameters.

        Raises:
            ValueError: If incorrect parameter types are provided.
        """
        try:
            self.validate_params(ticker, asset, start_time, end_time)

            params_dto = TradeParamsDTO(
                ticker=ticker, asset=asset, start_time=start_time, end_time=end_time
            )

            key = tuple(
                filter(
                    None,
                    [
                        "ticker" if ticker else None,
                        "asset" if asset else None,
                        "timerange" if start_time and end_time else None,
                    ],
                )
            )

            action_map = self.ACTIONS_OHLCV_MAP if ohlcv else self.ACTIONS_MAP
            action = action_map.get(key)

            if not action:
                raise ValueError("At least 'ticker' or 'asset' must be provided.")

            return TradeDTO(action=action, params=params_dto)

        except Exception as e:
            self.logger.error(
                f"Error building trade payload. Params: "
                f"ticker={ticker}, asset={asset}, start_time={start_time}, end_time={end_time}, ohlcv={ohlcv}. "
                f"Error: {e}"
            )
            raise RuntimeError(f"Unknown error building trade payload: {e}") from e

    @staticmethod
    def validate_params(ticker, interval, asset, start_time, end_time):
        """
        Validates the input parameters before processing.
        """
        if asset is not None and not isinstance(asset, str):
            raise ValueError(
                f"Expected 'asset' to be a string, but got {type(asset)}"
                f"Please, see the docs at section #GetTrades: README.md"
            )

        if ticker is not None and not isinstance(ticker, str):
            raise ValueError(
                f"Expected 'ticker' to be a string, but got {type(ticker)}"
                f"Please, see the docs at section #GetTrades: README.md"
            )
        if interval is not None and not isinstance(interval, TimescaleIntervalEnum):
            raise ValueError(
                f"Expected 'interval' to be a TimescaleEnum value, but got {type(interval)}"
                f"Please, see the docs at section #GetTrades: README.md"
            )

        if start_time is not None and not isinstance(start_time, datetime):
            raise ValueError(
                f"Expected 'start_time' to be a datetime, but got {type(start_time)}"
                f"Please, see the docs at section #GetTrades: README.md"
            )

        if end_time is not None and not isinstance(end_time, datetime):
            raise ValueError(
                f"Expected 'end_time' to be a datetime, but got {type(end_time)}"
                f"Please, see the docs at section #GetTrades: README.md"
            )
