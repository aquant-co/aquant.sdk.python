from dependency_injector import containers, providers

from aquant.core.dependencies.providers import create_logger_provider, init_nats_client
from aquant.domains.broker.service import BrokerService


class BrokerContainer(containers.DeclarativeContainer):
    """
    Dependency Injection Container for Broker
    """

    config = providers.Configuration()

    logger = providers.Singleton(create_logger_provider, name="BrokerService")

    nats_client = providers.Resource(
        init_nats_client,
        logger=logger,
        servers=config.nats_servers,
        user=config.nats_user,
        password=config.nats_password,
    )

    broker_service = providers.Factory(BrokerService, logger, nats_client)
