from dependency_injector import containers, providers

from aquant.core.dependencies.providers import create_logger_provider, init_nats_client
from aquant.domains.security.service import SecurityService


class SecurityContainer(containers.DeclarativeContainer):
    """
    Dependency Injection for Security
    """

    config = providers.Configuration()

    logger = providers.Singleton(create_logger_provider, name="SecurityService")

    nats_client = providers.Resource(
        init_nats_client,
        logger=logger,
        servers=config.nats_servers,
        user=config.nats_user,
        password=config.nats_password,
    )

    security_service = providers.Factory(SecurityService, logger, nats_client)
