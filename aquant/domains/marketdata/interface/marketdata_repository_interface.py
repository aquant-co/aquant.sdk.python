from abc import ABC, abstractmethod

import pandas as pd


class MarketdataRepositoryInterface(ABC):
    """
    Interface para obtenção de Market Data.
    """

    @abstractmethod
    def get_market_data(self, ticker: str) -> pd.DataFrame:
        """
        Obtém os dados de market data de um ativo específico.

        Args:
            ticker (str): O ativo a ser consultado.

        Returns:
            pd.DataFrame: Dados do ativo.
        """
        pass

    @abstractmethod
    def get_current_book(
        self, tickers: list[str], side: list[str] = None
    ) -> pd.DataFrame:
        """
        Consome dados do Redis.

        Args:
            tickers (list): Lista de chaves a serem consumidas.

        Returns:
            pd.DataFrame: DataFrame com os dados processados.
        """
        pass
