import firebase_admin
from dependency_injector import containers, providers
from firebase_admin import credentials

from src.infrastructure.services.firebase_auth_service_impl import FirebaseAuthService


class FirebaseContainer(containers.DeclarativeContainer):
    """Firebase services container."""

    # This container will receive the app_container's config as a dependency
    config = providers.Dependency()

    # Initialize Firebase with credentials from config
    firebase_credentials = providers.Factory(
        lambda config: (
            credentials.Certificate(config.firebase.credentials)
            if config.firebase.credentials
            else credentials.ApplicationDefault()
        ),
        config=config,
    )

    firebase_app = providers.Resource(
        firebase_admin.initialize_app,
        credential=firebase_credentials,
    )

    # Cleanup function
    cleanup = providers.Callable(
        lambda app: firebase_admin.delete_app(app) if app else None,
        app=firebase_app,
    )

    firebase_auth_service = providers.Singleton(FirebaseAuthService)
