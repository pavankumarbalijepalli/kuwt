from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_env() -> Environment:
    templates_dir = Path(__file__).resolve().parents[1] / "templates" / "email"
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def render_template(template_name: str, context: Dict[str, Any]) -> str:
    env = get_env()
    tmpl = env.get_template(template_name)
    return tmpl.render(**context)

