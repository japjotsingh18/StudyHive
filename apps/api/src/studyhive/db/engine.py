"""SQLAlchemy engine construction with no import-time connections."""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_database_engine(database_url: str) -> AsyncEngine:
    """Create the async engine; connections remain lazy until first use."""

    return create_async_engine(database_url, pool_pre_ping=True)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create the unit-of-work session factory for application repositories."""

    return async_sessionmaker(engine, expire_on_commit=False)
