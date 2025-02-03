from unittest.mock import MagicMock

from aquant.redis.consumer import RedisConsumer


def test_redis_consumer_on_demand():
    """
    Testa o RedisConsumer para consumo sob demanda,
    onde os valores de uma chave específica são buscados.
    """

    # Mockando o cliente Redis e o comportamento de leitura de dados via zrange
    mock_redis_client_instance = MagicMock()
    mock_redis_client_instance.zrange.side_effect = [
        [
            b'{"entry_time": "20250105102214.517", "price": 10.5, "quantity": 100}'
        ],  # APTI3_Bid
        [
            b'{"entry_time": "20250108125714.117", "price": 11.0, "quantity": 200}'
        ],  # APTI3_Offer
    ]

    mock_redis_client = MagicMock()
    mock_redis_client.get_client.return_value = mock_redis_client_instance

    # Mockando o processador de mensagens
    mock_processor = MagicMock()

    # Criando o RedisConsumer SEM `stream_key`
    consumer = RedisConsumer(
        redis_client=mock_redis_client,
        processor=mock_processor,
    )

    # Definindo as chaves para consumo
    keys = ["APTI3_Bid", "APTI3_Offer"]
    results = consumer.consume(keys)

    # Dados esperados
    expected_data = [
        {
            "key": "APTI3_Bid",
            "entry_time": "20250105102214.517",
            "price": 10.5,
            "quantity": 100,
        },
        {
            "key": "APTI3_Offer",
            "entry_time": "20250108125714.117",
            "price": 11.0,
            "quantity": 200,
        },
    ]

    # Validação dos resultados
    assert len(results) == len(expected_data), f"Resultados retornados: {results}"

    for idx, data in enumerate(expected_data):
        assert (
            results.iloc[idx].to_dict() == data
        ), f"Resultado incorreto para a posição {idx}: {results.iloc[idx].to_dict()}"

    # Verificando chamadas do processador
    calls = [
        mock_processor.process.call_args_list[0],
        mock_processor.process.call_args_list[1],
    ]

    assert (
        calls[0][0][0] == expected_data[0]
    ), f"Processador recebeu dado incorreto: {calls[0][0][0]}"
    assert (
        calls[1][0][0] == expected_data[1]
    ), f"Processador recebeu dado incorreto: {calls[1][0][0]}"

    print("✅ Teste de consumo sob demanda passou com sucesso.")
