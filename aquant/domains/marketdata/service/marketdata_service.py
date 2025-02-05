import pandas as pd

from aquant.domains.marketdata.repository import MarketdataRepository


class MarketdataService:
    """
    Service responsible for collecting and processing Market Data.
    """

    def __init__(self, repository: MarketdataRepository) -> None:
        """
        Initializes MarketdataService.

        Args:
            repository (MarketdataRepository): Instance of the market data repository.
        """
        self.repository = repository

    def get_market_data(self, ticker: str) -> pd.DataFrame:
        """
        Retrieves Market Data for a specific asset.

        Args:
            ticker (str): The asset to be queried.

        Returns:
            pd.DataFrame: Structured data of the asset.
        """
        raw_data = self.repository.get_market_data(ticker)
        return self._process_market_data(raw_data)

    def get_order_book(self, tickers: list[str]) -> pd.DataFrame:
        """
        Retrieves the order book for one or more assets.

        Args:
            tickers (list): List of assets to be queried.

        Returns:
            pd.DataFrame: Structured order book data.
        """
        raw_books = self.repository.consume_books(tickers)
        return self._process_order_book(raw_books)

    def _process_market_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes the retrieved market data.

        Args:
            df (pd.DataFrame): Raw market data.

        Returns:
            pd.DataFrame: Processed market data.
        """
        if df.empty:
            return df
        df["price"] = df["price"].astype(float)
        df["quantity"] = df["quantity"].astype(float)
        return df

    def _process_order_book(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes the retrieved order book data.

        Args:
            df (pd.DataFrame): Raw order book data.

        Returns:
            pd.DataFrame: Processed order book.
        """
        if df.empty:
            return df
        df["entry_time"] = pd.to_datetime(df["entry_time"])
        return df
