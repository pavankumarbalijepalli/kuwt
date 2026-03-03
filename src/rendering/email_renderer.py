from __future__ import annotations

from typing import Any, Dict, List, Sequence

from markupsafe import Markup
from markdown import markdown as md_to_html

from rendering.email_digest import EmailCard, Platform
from rendering.email_templates import render_template


def _markdown_to_html(markdown_text: str) -> str:
    return md_to_html(
        markdown_text or "",
        extensions=["fenced_code", "tables", "nl2br", "sane_lists"],
        output_format="html5",
    )


def render_platform_email_html(
    *,
    platform: Platform,
    date: str,
    cards: Sequence[EmailCard],
    kundelu_ai_png_url: str,
) -> str:
    rendered_cards: List[Dict[str, Any]] = []
    for c in cards:
        rendered_cards.append(
            {
                "title": c.title,
                "source": c.source,
                "content_html": Markup(_markdown_to_html(c.markdown)),
            }
        )

    template_name = f"{platform}.html.j2"
    return render_template(
        template_name,
        {
            "platform": platform,
            "date": date,
            "cards": rendered_cards,
            "kundelu_ai": kundelu_ai_png_url,
        },
    )

