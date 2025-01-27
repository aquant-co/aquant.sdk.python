from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


class CORSMiddlewareSetup:
    """
    Consfigures CORS settings for the application.
    """

    def __init__(
        self,
        allow_origins: list[str],
        allow_credentials: bool,
        allow_methods: list[str],
        allow_headers: list[str],
    ):
        """
        Initializes CORS settings.

        Args:
            allow_origins (list[str]): List of allowed origins.
            allow_credentials (bool): Wheather to allow credentials.
            allow_methods (list[str]): List of allowed methods.
            allow_headers (list[str]): List of allowed headers.
        """
        self.allow_origins = allow_origins
        self.allow_credentials = allow_credentials
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers

    def apply(self, app: FastAPI):
        """
        Applies the CORS settings to the application.

        Args:
            app: FastAPI application instance.
        """
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.allow_origins,
            allow_credentials=self.allow_credentials,
            allow_methods=self.allow_methods,
            allow_headers=self.allow_headers,
        )
