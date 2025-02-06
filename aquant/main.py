from datetime import datetime

import pandas as pd

from aquant.core.dependencies.containers import AquantContainer


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
        redis_use_tls: bool = True,
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
        redis_use_tls: bool = True,
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

        await self.initialize()
        return self

    async def initialize(self):
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
        self.marketdata = self.container.marketdata.marketdata_service()
        self.trade = await self.container.trade.trade_service()

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

    def get_current_order_book(self, tickers: list[str]) -> pd.DataFrame:
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
        return self.marketdata.get_order_book(tickers)

    async def get_trades(
        self, start_time: datetime, end_time: datetime
    ) -> pd.DataFrame:
        """
        Retrieves all trades within the specified time range.

        This asynchronous method fetches trade data between the provided start and end times.

        Args:
            start_time (datetime): The beginning of the time range for fetching trades.
            end_time (datetime): The end of the time range for fetching trades.

        Returns:
            pd.DataFrame: A DataFrame containing trade data within the specified time range.

        Example:
            ```python
            start_time = datetime(2023, 1, 1)
            end_time = datetime(2023, 1, 31)
            trades_df = await aquant.get_trades(start_time, end_time)
            print(trades_df)
            ```
        """
        return await self.trade.get_trades(start_time, end_time)
