import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.infrastructure.database.repr_mixin import ReprMixin

logger = logging.getLogger(__name__)


class Base(ReprMixin, DeclarativeBase):
    """Base class for all database models."""


def create_engine_and_sessionmaker(
    database_url: str, echo: bool = False, pool_size: int = 5, max_overflow: int = 10
):
    """Create a SQLAlchemy engine and sessionmaker.

    Args:
        database_url (str): The database URL.
        echo (bool): If True, SQLAlchemy will log all statements.
        pool_size (int): The size of the connection pool.
        max_overflow (int): The maximum number of connections to allow beyond the pool size.

    Returns:
        tuple: A tuple containing the engine and sessionmaker.
    """
    engine = create_async_engine(
        url=database_url,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=True,
    )

    sessionmaker = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False, class_=AsyncSession
    )

    return engine, sessionmaker
