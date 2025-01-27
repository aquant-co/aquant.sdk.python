from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_URL: str = ""
    REDIS_URL: str = ""
    APP_NAME: str = ""
    OPENAPI_URL: str = ""
    DEBUG: str = ""
    BASE_URL: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    CRYPTO_CONTEXT: str = ""
    CRYPTO_DEPRECATED: str = ""

    class Config:
        env_file = ".env"
