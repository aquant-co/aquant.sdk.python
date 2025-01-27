from functools import lru_cache

from app.core.config.settings import Settings


@lru_cache
def get_settings() -> Settings:
    """
    Provides a singleton instance of Settings loaded from environment variables.

    Returns:
        Settings: Application settings instance.
    """
    return Settings()
