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
    def consume_books(self, keys: list[str]) -> pd.DataFrame:
        """
        Consome dados do Redis.

        Args:
            keys (list): Lista de chaves a serem consumidas.

        Returns:
            pd.DataFrame: DataFrame com os dados processados.
        """
        pass
