from abc import ABC, abstractmethod
from typing import Any


class EmailService(ABC):
    @abstractmethod
    async def send_email(
        self, recipient: str, subject: str, template_name: str, context: dict[str, Any]
    ) -> None:
        """Send an email using a specified template and context.

        Args:
            recipient: The email address of the recipient.
            subject: The subject of the email.
            template_name: The name of the email template to use.
            context: A dictionary containing context variables for rendering the template.
        """
        pass
