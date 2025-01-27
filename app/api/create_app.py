from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.middleware import CORSMiddlewareSetup, LoggerMiddleware
from app.core.config import Settings
from app.ui.rest.routes.register_routes import register_routes


def _configure_middlewares(app: FastAPI):
    """
    Configures middleware for the application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.add_middleware(LoggerMiddleware)

    cors_config = CORSMiddlewareSetup(
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    cors_config.apply(app)


def create_app() -> FastAPI:
    """
    Initializes and configures the FastAPI application instance.

    Returns:
        FastAPI: Configured FastAPI application
    """
    settings = Settings()

    app = FastAPI(
        title="Aquant Bot API",
        version="1.0.0",
        description="Aquant Bot API",
        debug=bool(settings.DEBUG),
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    _configure_middlewares(app)
    register_routes(app)

    return app
