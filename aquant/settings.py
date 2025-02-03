from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str = ""
    DEBUG: str = ""
    BROKER_API: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
