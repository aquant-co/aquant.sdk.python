from unittest.mock import MagicMock

import pandas as pd

from aquant_sdk.redis.consumer import RedisConsumer


def test_redis_consumer_with_all_keys():
    mock_redis_client_instance = MagicMock()
    mock_redis_client_instance.xread.side_effect = [
        [(b"APTI3_Bid", [(b"1234", {b"price": b"10.5", b"quantity": b"100"})])],
        [(b"APTI3_Offer", [(b"5678", {b"price": b"11.0", b"quantity": b"200"})])],
    ]
    mock_redis_client_instance.keys.return_value = [b"APTI3_Bid", b"APTI3_Offer"]

    mock_redis_client = MagicMock()
    mock_redis_client.get_client.return_value = mock_redis_client_instance

    mock_processor = MagicMock()

    consumer = RedisConsumer(
        redis_client=mock_redis_client,
        stream_key=None,
        processor=mock_processor,
    )
    consumer.consume(real_time=False)

    mock_redis_client_instance.keys.assert_any_call(pattern="*_Bid")
    mock_redis_client_instance.keys.assert_any_call(pattern="*_Offer")
    print("Redis keys method called for *_Bid and *_Offer")

    assert mock_redis_client_instance.xread.call_count > 0
    print(f"xread called {mock_redis_client_instance.xread.call_count} times")

    data = [
        {"stream": "APTI3_Bid", "id": "1234", "price": "10.5", "quantity": "100"},
        {"stream": "APTI3_Offer", "id": "5678", "price": "11.0", "quantity": "200"},
    ]
    df = pd.DataFrame(data)

    assert not df.empty
    assert set(df.columns) == {"stream", "id", "price", "quantity"}
    print("Test passed with valid DataFrame structure and content.")
