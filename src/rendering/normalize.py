from __future__ import annotations

from typing import Any, Dict, List, Optional

from rendering.email_digest import EmailCard, Platform


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        # Many models store `{title, content}` blocks.
        if "content" in value and isinstance(value["content"], (str, int, float, bool)):
            return str(value["content"])
        return ""
    if isinstance(value, list):
        # Render list items as markdown bullets.
        items = [str(v) for v in value if v is not None]
        return "\n".join([f"- {i}" for i in items])
    return str(value)


def _md_kv(title: str, value: Any) -> str:
    text = _as_text(value).strip()
    if not text:
        return ""
    return f"### {title}\n{text}\n"


def _md_code(title: str, code: str) -> str:
    code = (code or "").strip()
    if not code:
        return ""
    return f"### {title}\n```python\n{code}\n```\n"


def build_platform_cards(
    *,
    researchers: Optional[Dict[str, Any]],
    enthusiasts: Optional[Dict[str, Any]],
    teachers: Optional[Dict[str, Any]],
) -> Dict[Platform, List[EmailCard]]:
    out: Dict[Platform, List[EmailCard]] = {
        "linkedin": [],
        "instagram": [],
        "medium": [],
        "youtube": [],
    }

    if researchers and isinstance(researchers, dict):
        for paper_title, payload in researchers.items():
            if not isinstance(payload, dict):
                continue

            li = payload.get("linkedin_post", {}) or {}
            li_md = "\n".join(
                filter(
                    None,
                    [
                        _md_kv("Hook", li.get("hook")),
                        _md_kv("Research Problem", li.get("research_problem")),
                        _md_kv("Key Insights", li.get("key_insights")),
                        _md_kv("Why it matters", li.get("why_it_matters")),
                        _md_kv("Closing reflection", li.get("closing_reflection")),
                        _md_kv("Hashtags", li.get("relavant_hashtags")),
                    ],
                )
            ).strip()
            if li_md:
                out["linkedin"].append(
                    EmailCard(title=paper_title, source="Research", markdown=li_md)
                )

            for platform_key, platform in [
                ("instagram_post", "instagram"),
                ("medium_post", "medium"),
                ("youtube_post", "youtube"),
            ]:
                p = payload.get(platform_key, {}) or {}
                if not isinstance(p, dict):
                    continue

                md_parts: List[str] = []
                for k, v in p.items():
                    if k in {"seo_tags", "hashtags", "relavant_hashtags", "tags"}:
                        md_parts.append(_md_kv(k.replace("_", " ").title(), v))
                    else:
                        md_parts.append(_md_kv(k.replace("_", " ").title(), v))
                md = "\n".join(filter(None, md_parts)).strip()
                if md:
                    out[platform].append(
                        EmailCard(title=paper_title, source="Research", markdown=md)
                    )

    if enthusiasts and isinstance(enthusiasts, dict):
        news_root = enthusiasts.get("news", {}) or {}
        news_item = news_root.get("news", {}) if isinstance(news_root, dict) else {}
        if isinstance(news_item, dict):
            for post_key, platform in [
                ("linkedin_post", "linkedin"),
                ("instagram_post", "instagram"),
                ("youtube_video", "youtube"),
            ]:
                content = news_item.get(post_key)
                if isinstance(content, dict):
                    md = "\n".join(
                        filter(
                            None,
                            [_md_kv(k.replace("_", " ").title(), v) for k, v in content.items()],
                        )
                    ).strip()
                    if md:
                        out[platform].append(
                            EmailCard(title="AI News", source="Enthusiast", markdown=md)
                        )

        repos_root = enthusiasts.get("repos", {}) or {}
        if isinstance(repos_root, dict):
            for repo_name, repo_payload in repos_root.items():
                if not isinstance(repo_payload, dict):
                    continue
                for post_key, platform in [
                    ("linkedin_post", "linkedin"),
                    ("instagram_post", "instagram"),
                    ("youtube_video", "youtube"),
                ]:
                    content = repo_payload.get(post_key)
                    if isinstance(content, dict):
                        md = "\n".join(
                            filter(
                                None,
                                [_md_kv(k.replace("_", " ").title(), v) for k, v in content.items()],
                            )
                        ).strip()
                        if md:
                            out[platform].append(
                                EmailCard(title=repo_name, source="Enthusiast", markdown=md)
                            )

    if teachers and isinstance(teachers, dict):
        for post_key, platform in [
            ("linkedin_post", "linkedin"),
            ("instagram_post", "instagram"),
            ("medium_post", "medium"),
            ("youtube_post", "youtube"),
        ]:
            t = teachers.get(post_key)
            if not isinstance(t, dict):
                continue

            title = t.get("title") or "Fundamentals"
            md_parts: List[str] = []
            for k, v in t.items():
                if k == "title":
                    continue
                if k == "walkthrough_code":
                    md_parts.append(_md_code("Walkthrough code", _as_text(v)))
                else:
                    md_parts.append(_md_kv(k.replace("_", " ").title(), v))
            md = "\n".join(filter(None, md_parts)).strip()
            if md:
                out[platform].append(
                    EmailCard(title=str(title), source="Teacher", markdown=md)
                )

    return out

