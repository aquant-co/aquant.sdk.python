from app.core.config.settings import Settings
from app.core.dependencies.logger import create_logger

settings = Settings()
logger = create_logger("cli_main")()
