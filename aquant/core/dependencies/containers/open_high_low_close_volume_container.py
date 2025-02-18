from dependency_injector import containers, providers

from aquant.core.dependencies.providers import create_logger_provider
from aquant.domains.trade.service import TradeOHLCVCalcService


class OpenHighLowClosedVolumeContainer(containers.DeclarativeContainer):
    """
    Dependency Injection Container for Open High Low Close Volume
    """

    logger = providers.Singleton(
        create_logger_provider, name="OpenHighLowCloseVolumeService"
    )

    open_high_low_close_volume_service = providers.Factory(
        TradeOHLCVCalcService, logger
    )
