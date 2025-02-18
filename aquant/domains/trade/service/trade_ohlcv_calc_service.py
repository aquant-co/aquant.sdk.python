import pandas as pd

from aquant.core.logger import Logger
from aquant.domains.trade.entity import OpenHighLowClosedVolume


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

    def calculate_ohlcv(self, df: pd.DataFrame) -> OpenHighLowClosedVolume:
        try:
            results = []
            grouped = df.groupby(["ticker", "asset"])
            for (ticker, asset), group in grouped:
                ohlcv = OpenHighLowClosedVolume(
                    ticker=ticker,
                    asset=asset,
                    open=self.calculate_open(group),
                    high=self.calculate_high(group),
                    low=self.calculate_low(group),
                    close=self.calculate_close(group),
                    volume=self.calculate_volume(group),
                )
                results.append(ohlcv.dict(by_alias=True))
            return results
        except Exception as e:
            self.logger.error(f"Error trying to calculate OHLCV: {e}")
            return []
