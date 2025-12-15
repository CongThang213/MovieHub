from dependency_injector import containers, providers

from src.infrastructure.database.init_database import create_engine_and_sessionmaker


class DatabaseContainer(containers.DeclarativeContainer):
    """Database container for dependency injection."""

    # This container will receive the app_container as a dependency
    config = providers.Dependency()

    # Create engine and sessionmaker using the config from the app_container
    _engine_and_sessionmaker = providers.Factory(
        create_engine_and_sessionmaker,
        database_url=config.provided.database.url_async,
        echo=config.provided.database.echo,
        pool_size=config.provided.database.pool_size,
        max_overflow=config.provided.database.max_overflow,
    )

    engine = providers.Resource(
        lambda result: result[0],
        _engine_and_sessionmaker,
    )

    sessionmaker = providers.Resource(
        lambda result: result[1],
        _engine_and_sessionmaker,
    )
