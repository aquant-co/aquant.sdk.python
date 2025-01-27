import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from app.core.config import Settings

# Load settings for secret key and algorithm
settings = Settings()

def generate_jwt(payload: Dict[str, Any], expires_delta: timedelta = timedelta(hours=1)) -> str:
    """
    Generates a JSON Web Token (JWT).

    Args:
        payload (Dict[str, Any]): The payload for the JWT.
        expires_delta (timedelta): The duration until the token expires.

    Returns:
        str: The generated JWT.
    """
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  # type: ignore
    return encoded_jwt


def decode_jwt(token: str) -> Dict[str, Any]:
    """
    Decodes and validates a JSON Web Token (JWT).

    Args:
        token (str): The JWT to decode.

    Returns:
        Dict[str, Any]: The payload of the decoded JWT.

    Raises:
        ValueError: If the token is expired or invalid.
    """
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  # type: ignore
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token.")
