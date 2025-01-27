from fastapi import FastAPI

from app.ui.rest.routes.monitoring.health_check import router as health_check_router
from app.ui.rest.routes.users import router as user_router


def register_routes(app: FastAPI):
    """
    Registers all API webhooks routes.

    Args:
        app (FastAPI): FastAPI application instance.
    """
    app.include_router(user_router, prefix="/users", tags=["User", "Login"])
    app.include_router(
        health_check_router, prefix="/monitoring", tags=["Monitoring", "HealthCheck"]
    )
