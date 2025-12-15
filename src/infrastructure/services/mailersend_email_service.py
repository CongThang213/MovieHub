from typing import Any

from mailersend import MailerSendClient, EmailBuilder

from config.app_config import AppSettings
from src.application.engines.template_render_engine import RenderEngine
from src.application.services.email_service import EmailService


class MailerSendEmailService(EmailService):
    def __init__(self, config: AppSettings, render_engine: RenderEngine):
        self._config = config
        self._render_engine = render_engine
        self._mailer = MailerSendClient(api_key=config.mailersend.api_key)

    async def send_email(
        self, recipient: str, subject: str, template_name: str, context: dict[str, Any]
    ) -> None:
        """Send an email using MailerSend API with template rendering.

        Args:
            recipient: The email address of the recipient.
            subject: The subject of the email.
            template_name: The name of the template file to render.
            context: Variables to be substituted in the template.
        """
        # Render the HTML content using the Jinja template engine
        html_content = self._render_engine.render(template_name, context)

        # Create the email using EmailBuilder
        email = (
            EmailBuilder()
            .from_email(
                self._config.mailersend.email,
                self._config.project.name,
            )
            .to_many([{"email": recipient}])
            .subject(subject)
            .html(html_content)
            .build()
        )

        try:
            response = self._mailer.emails.send(email)

            if hasattr(response, "status_code") and response.status_code >= 400:
                error_message = (
                    response.text if hasattr(response, "text") else "Unknown error"
                )
                raise Exception(f"Failed to send email: {error_message}")

        except Exception as e:
            # Log the error but don't raise it to the caller
            # This prevents email failures from breaking application flow
            from config.logging_config import logger

            logger.error(f"Error sending email to {recipient}: {str(e)}")
