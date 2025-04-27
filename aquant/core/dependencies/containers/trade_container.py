from dependency_injector import containers, providers

from aquant.core.dependencies.providers import create_logger_provider, init_nats_client
from aquant.domains.trade.service import (
    OpenHighLowCloseVolumeBinaryCodec,
    TradeBinaryCodec,
    TradeBinaryRequestCodec,
    TradeParserService,
    TradePayloadBuilderService,
    TradeService,
)


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
    trade_binary_codec = providers.Singleton(TradeBinaryCodec, logger)
    trade_request_codec = providers.Singleton(TradeBinaryRequestCodec, logger)
    ohlcv_binary_codec = providers.Singleton(OpenHighLowCloseVolumeBinaryCodec, logger)

    trade_payload_builder_service = providers.Factory(
        TradePayloadBuilderService, logger
    )
    trade_parser_service = providers.Factory(
        TradeParserService,
        logger,
        trade_codec=trade_binary_codec,
        trade_request_codec=trade_request_codec,
        ohlcv_codec=ohlcv_binary_codec,
    )

    trade_service = providers.Factory(
        TradeService,
        logger,
        nats_client,
        trade_payload_builder_service,
        trade_parser_service,
    )
