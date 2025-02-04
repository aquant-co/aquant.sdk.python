from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str = ""
    DEBUG: str = ""
    BROKER_API: str = ""
    NATS_URL: str = ""
    AQUANT_NATS_USER: str = ""
    AQAUNT_NATS_PASSWORD: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
