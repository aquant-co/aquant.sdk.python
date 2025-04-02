from datetime import datetime

import pandas as pd

from aquant.core.dependencies.containers import AquantContainer
from aquant.domains.trade.entity import OpenHighLowCloseVolume


class Aquant:
    """
    The main entry point for the Aquant SDK, facilitating automatic dependency injection.

    This class initializes and manages connections to Redis and NATS servers, providing
    methods to interact with market data and trade services.

    Attributes:
        container (AquantContainer): The dependency injection container for managing services.
        marketdata: Service for accessing market data functionalities.
        trade: Service for accessing trade-related functionalities.

    Args:
        redis_url (str): The connection URL for the Redis server.
        nats_servers (list[str]): A list of NATS server URLs.
        nats_user (str): Username for NATS authentication.
        nats_password (str): Password for NATS authentication.
        redis_use_tls (bool, optional): Indicates whether to use TLS for Redis connections. Defaults to True.

    Example:
        ```python
        aquant = Aquant(
            redis_url="redis://localhost:6379",
            nats_servers=["nats://localhost:4222"],
            nats_user="your_nats_user",
            nats_password="..."
        )
        await aquant.initialize()
        ```
    """

    def __init__(
        self,
        redis_url: str,
        nats_servers: list[str],
        nats_user: str,
        nats_password: str,
        redis_use_tls: bool = False,
    ) -> None:
        """
        Initializes the Aquant instance with the provided configuration.

        This method sets up the configuration for Redis and NATS connections
        and prepares the dependency injection container.

        Args:
            redis_url (str): The connection URL for the Redis server.
            nats_servers (list[str]): A list of NATS server URLs.
            nats_user (str): Username for NATS authentication.
            nats_password (str): Password for NATS authentication.
            redis_use_tls (bool, optional): Indicates whether to use TLS for Redis connections. Defaults to True.
        """
        self.container = AquantContainer()
        self.container.config.redis_url.from_value(redis_url)
        self.container.config.redis_use_tls.from_value(redis_use_tls)
        self.container.config.nats_servers.from_value(nats_servers)
        self.container.config.nats_user.from_value(nats_user)
        self.container.config.nats_password.from_value(nats_password)

    @classmethod
    async def create(
        cls,
        redis_url: str,
        nats_servers: list[str],
        nats_user: str,
        nats_password: str,
        redis_use_tls: bool = False,
    ):
        """
        Factory asynchronous method for create and initialize one Aquant instance

        Args:
            redis_url (str): The connection URL for the Redis server.
            nats_servers (list[str]): A list of NATS server URLs.
            nats_user (str): Username for NATS authentication.
            nats_password (str): Password for NATS authentication.
            redis_use_tls (bool, optional): Indicates whether to use TLS for Redis connections. Defaults to True.
        Returns:
            Aquant: One Aquant instance initialized.
        """
        self = cls(
            redis_url,
            nats_servers,
            nats_user,
            nats_password,
            redis_use_tls,
        )

        await self._initialize()
        return self

    async def _initialize(self):
        """
        Initializes and wires the necessary services.

        This asynchronous method wires the dependency injection container and
        initializes the market data and trade services for subsequent operations.

        Example:
            ```python
            await aquant.initialize()
            ```
        """
        self.container.wire(modules=[__name__])
        self.marketdata = await self.container.marketdata.marketdata_service()
        self.trade = await self.container.trade.trade_service()
        self.trade_payload_builder_service = (
            self.container.trade.trade_payload_builder_service()
        )
        self.trade_parser_service = self.container.trade.trade_parser_service()
        self.open_high_low_close_volume = (
            self.container.open_high_low_close_volume.open_high_low_close_volume_service()
        )
        self.broker = await self.container.broker.broker_service()
        self.security = await self.container.security.security_service()

    def shutdown(self):
        """
        Unwires and cleans up resources.

        This method unwires the dependency injection container, effectively
        releasing any resources held by the services.

        Example:
            ```python
            aquant.shutdown()
            ```
        """
        self.container.unwire()

    def get_current_order_book(
        self, tickers: list[str], max_entries: int = 20
    ) -> pd.DataFrame:
        """
        Retrieves the current order book for the specified tickers.

        Args:
            tickers (list[str]): A list of ticker symbols to retrieve the order book for.

        Returns:
            pd.DataFrame: A DataFrame containing the order book data for the specified tickers.

        Example:
            ```python
            order_book_df = aquant.get_current_order_book(["AAPL", "MSFT"])
            print(order_book_df)
            ```
        """
        return self.marketdata.get_order_book(tickers, max_entries)

    async def get_trades(
        self,
        ticker: str | None = None,
        asset: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        ohlcv: bool = False,
    ) -> pd.DataFrame | OpenHighLowCloseVolume:
        """
        Retrieves all trades within the specified time range.

        This asynchronous method fetches trade data based on the provided parameters.

        Args:
            ticker (Optional[str]): The ticker symbol for the asset.
            asset (Optional[str]): The asset identifier.
            start_time (Optional[datetime]): The beginning of the time range for fetching trades.
            end_time (Optional[datetime]): The end of the time range for fetching trades.
            ohlcv (bool): If True, returns OHLCV (Open-High-Low-Close-Volume) data instead of raw trade data.

        Returns:
            Optional[pd.DataFrame]: A DataFrame containing trade data or None if invalid parameters are provided.
            OpenHighLowCloseVolume: A class containing ohlcv results or None if an error has raised.

        Raises:
            ValueError: If neither 'ticker' nor 'asset' is provided, or if start_time > end_time.

        Example:
            ```python
            ticker = "AAPL"
            start_time = datetime(2023, 1, 1)
            end_time = datetime(2023, 1, 31)
            trades_df = await aquant.get_trades(ticker=ticker, start_time=start_time, end_time=end_time)
            return trades_df
            ```
        """

        if not ticker and not asset and not start_time and not end_time:
            raise ValueError(
                "At least one of 'ticker' or 'asset', or 'start_time', and or 'end_time' must be provided."
            )

        if start_time and end_time and start_time > end_time:
            raise ValueError("start_time cannot be greater than end_time.")

        return await self.trade.get_trades(
            ticker=ticker,
            asset=asset,
            start_time=start_time,
            end_time=end_time,
            ohlcv=ohlcv,
        )

    async def get_broker(self, fk_id: int) -> pd.DataFrame:
        """
        Retrieves broker information based on the given foreign key ID.

        This asynchronous method queries the broker service to fetch broker details
        associated with the specified foreign key ID (fk_id).

        Args:
            fk_id (int): The foreign key ID of the broker.

        Returns:
            pd.DataFrame: A DataFrame containing broker details.

        Raises:
            ValueError: If the provided fk_id is invalid or not found.

        Example:
            ```python
            fk_id = 1234
            broker_info = await aquant.get_broker(fk_id=fk_id)
            print(broker_info)
            ```
        """
        return await self.broker.get_broker_by_fk_id(fk_id)

    async def get_securities(
        self, ticker: str = None, asset: str = None, expires_at: datetime = None
    ) -> dict:
        """
        Fetches security details based on ticker, asset, or expiration date.

        This asynchronous method queries the security service to retrieve security
        information for a given ticker, asset name, or expiration date.

        Args:
            ticker (Optional[str]): The ticker symbol of the security.
            asset (Optional[str]): The name of the asset associated with the security.
            expires_at (Optional[datetime]): The expiration date of the security.

        Returns:
            dict: A dictionary containing security details.

        Raises:
            ValueError: If none of the parameters are provided or if the query fails.

        Example:
            ```python
            ticker = "VALE3"
            asset = "VALE"
            expires_at = datetime(2025, 12, 31)

            security_info = await aquant.get_securities(ticker=ticker, asset=asset, expires_at=expires_at)
            print(security_info)
            ```
        """
        return await self.security.get_securities(ticker, asset, expires_at)

    """
    Auxiliary functions for OHLCV calculations in DataFrames.

    These methods provide an interface to compute individual components of OHLCV
    (Open, High, Low, Close, Volume) from a given DataFrame containing trade data.
    They interact with the `open_high_low_close_volume` service to perform calculations.

    Each function extracts the corresponding OHLCV value from the dataset, ensuring
    that users can efficiently process and analyze market data.
    """

    def calculate_ohlcv_open(self, df) -> float:
        """
        Calculates the open price from the given trade DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing trade data.

        Returns:
            float: The first recorded trade price (open price).

        Example:
            ```python
            open_price = aquant.calculate_ohlcv_open(df)
            print(open_price)
            ```
        """
        return self.open_high_low_close_volume.calculate_open(df)

    def calculate_ohlcv_high(self, df) -> float:
        """
        Calculates the highest trade price (high) from the given trade DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing trade data.

        Returns:
            float: The highest recorded trade price.

        Example:
            ```python
            high_price = aquant.calculate_ohlcv_high(df)
            print(high_price)
            ```
        """
        return self.open_high_low_close_volume.calculate_high(df)

    def calculate_ohlcv_low(self, df) -> float:
        """
        Calculates the lowest trade price (low) from the given trade DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing trade data.

        Returns:
            float: The lowest recorded trade price.

        Example:
            ```python
            low_price = aquant.calculate_ohlcv_low(df)
            print(low_price)
            ```
        """
        return self.open_high_low_close_volume.calculate_low(df)

    def calculate_ohlcv_close(self, df) -> float:
        """
        Calculates the closing trade price from the given trade DataFrame.

        The close price is the last recorded trade price in the dataset.

        Args:
            df (pd.DataFrame): The DataFrame containing trade data.

        Returns:
            float: The last recorded trade price (close price).

        Example:
            ```python
            close_price = aquant.calculate_ohlcv_close(df)
            print(close_price)
            ```
        """
        return self.open_high_low_close_volume.calculate_close(df)

    def calculate_ohlcv_volume(self, df) -> float:
        """
        Calculates the total trade volume from the given trade DataFrame.

        This method sums all trade quantities within the dataset.

        Args:
            df (pd.DataFrame): The DataFrame containing trade data.

        Returns:
            float: The total trade volume.

        Example:
            ```python
            total_volume = aquant.calculate_ohlcv_volume(df)
            print(total_volume)
            ```
        """
        return self.open_high_low_close_volume.calculate_volume(df)

    def calculate_ohlcv(self, df) -> dict:
        """
        Computes the complete OHLCV values (Open, High, Low, Close, Volume) from the given DataFrame.

        This method consolidates all OHLCV calculations into a single dictionary structure.

        Args:
            df (pd.DataFrame): The DataFrame containing trade data.

        Returns:
            dict: A dictionary with OHLCV values.

        Example:
            ```python
            ohlcv_data = aquant.calculate_ohlcv(df)
            print(ohlcv_data)
            ```
        """
        return self.open_high_low_close_volume.calculate_ohlcv(df)
