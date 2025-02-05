def validate_stream_key(stream_key: str):
    if not stream_key:
        raise ValueError("stream_key can not be empty")
