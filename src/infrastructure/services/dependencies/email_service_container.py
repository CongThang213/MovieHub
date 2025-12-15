from dependency_injector import containers, providers

from src.infrastructure.engines.jinja_render_engine import JinJaRenderEngine
from src.infrastructure.services.mailersend_email_service import MailerSendEmailService


class EmailServiceContainer(containers.DeclarativeContainer):
    """Container for email service dependencies."""

    # This container will receive the app_container's config as a dependency
    config = providers.Dependency()

    # Create template render engine
    template_render_engine = providers.Singleton(
        JinJaRenderEngine, template_dir="templates/emails"
    )

    # Create email service with config and render engine
    email_service = providers.Singleton(
        MailerSendEmailService, config=config, render_engine=template_render_engine
    )
