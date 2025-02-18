import pandas as pd

from aquant.core.logger import Logger
from aquant.domains.trade.entity import OpenHighLowCloseVolume


class TradeOHLCVCalcService:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def calculate_open(self, df: pd.DataFrame) -> float:
        try:
            return df.iloc[0]["price"]
        except Exception as e:
            self.logger.error(f"Error trying to calculate ohlcv - open. Error : {e}")

    def calculate_high(self, df: pd.DataFrame) -> float:
        try:
            return df["price"].max()
        except Exception as e:
            self.logger.error(f"Error trying to calculate ohlcv - open. Error : {e}")

    def calculate_low(self, df: pd.DataFrame) -> float:
        try:
            return df["price"].min()
        except Exception as e:
            self.logger.error(f"Error trying to calculate ohlcv - open. Error : {e}")

    def calculate_close(self, df: pd.DataFrame) -> float:
        try:
            return df.iloc[-1]["price"]
        except Exception as e:
            self.logger.error(f"Error trying to calculate ohlcv - open. Error : {e}")

    def calculate_volume(self, df: pd.DataFrame) -> float:
        try:
            return df["quantity"].sum()
        except Exception as e:
            self.logger.error(f"Error trying to calculate ohlcv - open. Error : {e}")

    def calculate_ohlcv(self, df: pd.DataFrame) -> OpenHighLowCloseVolume:
        try:
            ohlcv = OpenHighLowCloseVolume(
                open=self.calculate_open(df),
                high=self.calculate_high(df),
                low=self.calculate_low(df),
                close=self.calculate_close(df),
                volume=self.calculate_volume(df),
            )
            return ohlcv
        except Exception as e:
            self.logger.error(f"Error trying to calculate OHLCV: {e}")
            return []
