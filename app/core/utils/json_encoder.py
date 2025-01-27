from typing import Any
from uuid import UUID


def custom_json_encoder(obj: Any):
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")
