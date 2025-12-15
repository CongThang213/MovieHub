from dependency_injector import containers, providers

from config.redis_config import RedisSettings
from src.infrastructure.services.redis_service import RedisService
from src.infrastructure.services.websocket_manager import WebsocketManager


class RedisContainer(containers.DeclarativeContainer):
    """Container for Redis-related dependencies."""

    config = providers.Dependency()

    redis_settings = providers.Singleton(RedisSettings)

    redis_service = providers.Singleton(
        RedisService,
        redis_url=redis_settings.provided.url,
    )

    websocket_manager = providers.Singleton(
        WebsocketManager,
        redis_service=redis_service,
    )
