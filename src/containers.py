from dependency_injector import containers, providers
from dependency_injector.providers import Singleton, Container

from config.app_config import AppSettings
from src.application.use_cases.dependencies.containers import UseCaseContainer
from src.infrastructure.database.dependencies.container import DatabaseContainer
from src.infrastructure.gateway.dependencies.payment_gateway_container import (
    PaymentGatewayContainer,
)
from src.infrastructure.repositories.dependencies.containers import RepositoryContainer
from src.infrastructure.services.dependencies.auth_service_containers import (
    FirebaseContainer,
)
from src.infrastructure.services.dependencies.email_service_container import (
    EmailServiceContainer,
)
from src.infrastructure.services.dependencies.image_service_container import (
    CloudinaryContainer,
)
from src.infrastructure.services.dependencies.redis_service_container import (
    RedisContainer,
)


class AppContainer(containers.DeclarativeContainer):
    """Global application container for dependency injection."""

    # settings are loaded from the environment variables
    config: Singleton[AppSettings] = providers.Singleton(AppSettings)

    # Create the database container and inject the config
    database_settings: Container[DatabaseContainer] = providers.Container(
        DatabaseContainer, config=config
    )

    # Create the Firebase container and inject the config
    firebase: Container[FirebaseContainer] = providers.Container(
        FirebaseContainer, config=config
    )

    # Create the Cloudinary container and inject the config
    cloudinary: Container[CloudinaryContainer] = providers.Container(
        CloudinaryContainer, config=config
    )

    # Create the Email service container and inject the config
    email: Container[EmailServiceContainer] = providers.Container(
        EmailServiceContainer, config=config
    )

    # Create the Redis container and inject the config
    redis: Container[RedisContainer] = providers.Container(
        RedisContainer, config=config
    )

    # Create the Payment Gateway container and inject the config
    payment_gateway: Container[PaymentGatewayContainer] = providers.Container(
        PaymentGatewayContainer, config=config
    )

    # Create the repository container and inject the config
    # This container will receive the database as dependencies
    # and will use them to create the repositories
    repositories: Container[RepositoryContainer] = providers.Container(
        RepositoryContainer,
        database=database_settings,
    )

    # Create the use case container and inject repositories and services directly
    use_cases: Container[UseCaseContainer] = providers.Container(
        UseCaseContainer,
        repositories=repositories,
        firebase=firebase,
        cloudinary=cloudinary,
        email=email,
        database=database_settings,
        payment_gateway=payment_gateway,
        config=config,
    )
