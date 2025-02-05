import pandas as pd

from aquant.core.dependencies.containers import AquantContainer


class Aquant:
    """
    Entry point for the Aquant SDK, automatically injecting dependencies.

    Args:
    redis_url (str): Redis connection URL.
    redis_user (str, optional): Redis username.
    redis_password (str, optional): Redis password.
    """

    def __init__(self, redis_url: str, redis_use_tls: bool = True) -> None:
        self.container = AquantContainer()
        self.container.config.redis_url.from_value(redis_url)
        self.container.config.redis_use_tls.from_value(redis_use_tls)

        self.marketdata = self.container.marketdata.marketdata_service()

    def get_order_book(self, tickers: list[str]) -> pd.DataFrame:
        """
        Gathers the order book for one or more tickers.

        Args:
            tickers (list[str]): List one, or more of tickers to be queried.

        Returns:
            pd.DataFrame: Structured order book data
        """
        return self.marketdata.get_order_book(tickers)
