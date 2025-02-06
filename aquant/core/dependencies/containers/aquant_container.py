from dependency_injector import containers, providers

from aquant.core.dependencies.containers.marketdata_container import MarketdataContainer
from aquant.core.dependencies.containers.trade_container import TradeContainer


class AquantContainer(containers.DeclarativeContainer):
    """
    Main Dependency Injection Container for Aquant SDK.
    """

    config = providers.Configuration()

    marketdata = providers.Container(MarketdataContainer, config=config)
    trade = providers.Container(TradeContainer, config=config)
