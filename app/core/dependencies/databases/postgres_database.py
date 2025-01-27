from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import PostgresDatabase

postgres_db = PostgresDatabase()


async def get_postgres_db() -> AsyncSession:
    """
    Provides a database session for PostgreSQL.

    Yields:
        AsyncSession: SQLAlchemy async session.
    """
    session_factory = postgres_db.get_client()
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
