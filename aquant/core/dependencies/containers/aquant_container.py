from dependency_injector import containers, providers

from aquant.core.dependencies.containers.broker_container import BrokerContainer
from aquant.core.dependencies.containers.marketdata_container import MarketdataContainer
from aquant.core.dependencies.containers.open_high_low_close_volume_container import (
    OpenHighLowClosedVolumeContainer,
)
from aquant.core.dependencies.containers.security_container import SecurityContainer
from aquant.core.dependencies.containers.trade_container import TradeContainer


class AquantContainer(containers.DeclarativeContainer):
    """
    Main Dependency Injection Container for Aquant SDK.
    """

    config = providers.Configuration()

    marketdata = providers.Container(MarketdataContainer, config=config)
    trade = providers.Container(TradeContainer, config=config)
    broker = providers.Container(BrokerContainer, config=config)
    security = providers.Container(SecurityContainer, config=config)
    open_high_low_close_volume = providers.Container(OpenHighLowClosedVolumeContainer)
