import cloudinary
from dependency_injector import containers, providers

from src.infrastructure.services.cloudinary_image_service_impl import (
    CloudinaryImageService,
)


class CloudinaryContainer(containers.DeclarativeContainer):
    """Container for cloudinary storage service."""

    # This container will receive the app_container's config as a dependency
    config = providers.Dependency()

    # Create and configure the Cloudinary app instance using the provided config
    # cloudinary.config sets global configuration and returns None, so use Callable.
    cloudinary_app = providers.Callable(
        cloudinary.config,
        cloud_name=config.provided.cloudinary.cloud_name,
        api_key=config.provided.cloudinary.api_key,
        api_secret=config.provided.cloudinary.api_secret,
        secure=config.provided.cloudinary.secure,
    )

    cloudinary_image_service = providers.Singleton(
        CloudinaryImageService, config=config
    )
