from typing import Any

from jinja2 import Environment, FileSystemLoader

from src.application.engines.template_render_engine import RenderEngine


class JinJaRenderEngine(RenderEngine):
    def __init__(self, template_dir: str = "templates/emails"):
        self._env = Environment(loader=FileSystemLoader(template_dir))

    def render(self, template_name: str, context: dict[str, Any]) -> str:
        return self._env.get_template(template_name).render(**context)
