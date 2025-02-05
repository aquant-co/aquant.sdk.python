from .brokers_dict import BROKER_DATA

broker_cache: dict[int, str] = {}


def get_brokers_name_mock(broker_id: int, use_cache: bool = True) -> str:
    """
    Mock para simular a busca de nome de brokers com suporte a cache.

    Args:
        broker_id (int): ID do broker.
        use_cache (bool): Define se o cache deve ser usado. Default é True.

    Returns:
        str: Nome do broker ou uma mensagem padrão se não encontrado.
    """
    if use_cache and broker_id in broker_cache:
        return broker_cache[broker_id]

    broker_data = BROKER_DATA.get(broker_id)
    if broker_data:
        broker_name = broker_data["name"]
        if use_cache:
            broker_cache[broker_id] = broker_name
        return broker_name
    else:
        return "Broker not found"
