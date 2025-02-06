from dependency_injector import containers, providers

from aquant.core.dependencies.providers import create_logger_provider, init_nats_client
from aquant.domains.trade.service import TradeService


class TradeContainer(containers.DeclarativeContainer):
    """
    Dependency Injection Container for Trade
    """

    config = providers.Configuration()

    logger = providers.Singleton(create_logger_provider, name="TradeService")

    nats_client = providers.Resource(
        init_nats_client,
        logger=logger,
        servers=config.nats_servers,
        user=config.nats_user,
        password=config.nats_password,
    )

    trade_service = providers.Factory(TradeService, logger, nats_client)
