from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_URL: str = ""
    DEBUG: str = ""
    BROKER_API: str = ""
    NATS_URL: str = ""
    AQUANT_NATS_USER: str = ""
    AQUANT_NATS_PASSWORD: str = ""
    LOG_LEVEL: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
