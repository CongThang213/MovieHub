from config.app_config import AppSettings
from config.logging_config import logger
from src.application.exceptions.auth_exceptions import (
    AuthenticationError,
)
from src.application.services.auth_service import AuthService
from src.application.services.email_service import EmailService


class ForgotPasswordUseCase:
    def __init__(
        self,
        auth_service: AuthService,
        email_service: EmailService,
        config: AppSettings,
    ) -> None:
        self._auth_service = auth_service
        self._email_service = email_service
        self._project_name = config.project.name

    async def execute(self, email: str) -> None:
        """Execute the forgot password use case to send a password reset email.

        This method performs the following steps:
            1. Validate the email
            2. Request Firebase to send a password reset email

        Args:
            email (str): The email address of the user requesting password reset.

        Raises:
            AuthenticationError: If sending the password reset email fails.
        """
        try:
            logger.debug(f"Sending password reset email to: {email}")
            rt_pass_context = self._auth_service.generate_password_reset_link(email)
            rt_pass_context["project_name"] = self._project_name
            await self._email_service.send_email(
                recipient=email,
                context=rt_pass_context,
                subject="Đặt lại mật khẩu tài khoản",
                template_name="password_reset_template.html",
            )
            logger.success(f"Password reset email sent successfully to: {email}")
        except AuthenticationError as e:
            logger.error(f"Password reset failed due to authentication error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during password reset: {str(e)}")
            raise AuthenticationError("Failed to process password reset")
