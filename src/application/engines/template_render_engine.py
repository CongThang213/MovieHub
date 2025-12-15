from abc import ABC, abstractmethod
from typing import Any


class RenderEngine(ABC):
    """Abstract base class for a template rendering engine."""

    @abstractmethod
    def render(self, template_name: str, context: dict[str, Any]) -> str:
        """Render a template with the given context.

        Args:
            template_name: The name of the template to render.
            context: A dictionary containing context variables for rendering the template.

        Returns:
            The rendered template as a string.
        """
        pass
