from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config.settings import Settings
from app.core.database import DatabaseInterface


class PostgresDatabase(DatabaseInterface):
    """
    PostgreSQL implementation of DatabaseInterface using SQLAlchemy.

    Attributes:
        engine: SQLAlchemy engine instance
        session: SQLAlchemy session maker for creating database sessions
    """

    def __init__(self, db_url: str = None, debug: bool = None):
        settings = Settings()
        self.engine = create_async_engine(
            db_url or str(settings.POSTGRES_URL),
            future=True,
            echo=debug or bool(settings.DEBUG),
        )
        self.session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession
        )

    async def connect(self) -> None:
        """
        Establishes the database connection
        (No explicit connection needed for SQLAlchemy).
        """

    async def disconnect(self) -> None:
        """
        Closes the database connection and releases resources.
        """
        await self.engine.dispose()

    def get_client(self) -> sessionmaker:
        """
        Returns the PostgreSQL session factory.

        Returns:
            sessionmaker: SQLAlchemy session factory.
        """
        return self.session
