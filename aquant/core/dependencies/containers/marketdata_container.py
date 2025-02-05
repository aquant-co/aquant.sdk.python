from dependency_injector import containers, providers

from aquant.core.dependencies.providers import create_logger_provider
from aquant.domains.marketdata.repository import MarketdataRepository
from aquant.domains.marketdata.service import MarketdataService
from aquant.infra.redis import BufferedMessageProcessor, RedisClientFactory


class MarketdataContainer(containers.DeclarativeContainer):
    """
    Dependency Injection Container for Marketdata.
    """

    config = providers.Configuration()

    logger = providers.Singleton(create_logger_provider, name="Marketdata")
    processor = providers.Singleton(BufferedMessageProcessor)

    redis_client = providers.Singleton(
        RedisClientFactory.create_client,
        redis_url=config.redis_url,
        use_tls=config.redis_use_tls,
    )

    marketdata_repository = providers.Factory(
        MarketdataRepository,
        redis_client=redis_client,
        processor=processor,
        logger=logger,
    )

    marketdata_service = providers.Factory(
        MarketdataService, repository=marketdata_repository
    )
