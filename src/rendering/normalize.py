from __future__ import annotations

from typing import Any, Dict, List, Optional

from rendering.post_digest import PostCard, Platform


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
    return f"{text}\n"


def _md_code(title: str, code: str) -> str:
    code = (code or "").strip()
    if not code:
        return ""
    return f"```python\n{code}\n```\n"


def build_platform_cards(
    *,
    researchers: Optional[Dict[str, Any]],
    enthusiasts: Optional[Dict[str, Any]],
    teachers: Optional[Dict[str, Any]],
) -> Dict[Platform, List[PostCard]]:
    out: Dict[Platform, List[PostCard]] = {
        "linkedin": [],
        "instagram": [],
        "medium": [],
        "youtube": [],
    }

    if researchers and isinstance(researchers, dict):
        for paper_title, payload in researchers.items():
            if not isinstance(payload, dict):
                continue

            for platform_key, platform in [
                ("linkedin_post", "linkedin"),
                ("instagram_post", "instagram"),
                ("medium_post", "medium"),
                ("youtube_post", "youtube"),
            ]:
                p = payload.get(platform_key, {}) or {}
                if not isinstance(p, dict):
                    continue

                if platform == "instagram":
                    md = _render_instagram_script(p)
                elif platform == "linkedin":
                    md = _render_linkedin_post(p)
                elif platform == "medium":
                    md = _render_medium_article(p)
                elif platform == "youtube":
                    md = _render_youtube_script(p)
                else:
                    md = ""

                if md:
                    out[platform].append(
                        PostCard(title=paper_title, source="Research", markdown=md)
                    )

    if enthusiasts and isinstance(enthusiasts, dict):
        news_root = enthusiasts.get("news", {}) or {}
        news_item = news_root.get("news", {}) if isinstance(news_root, dict) else {}
        if isinstance(news_item, dict):
            for post_key, platform in [
                ("linkedin_post", "linkedin"),
                ("instagram_post", "instagram"),
                ("youtube_post", "youtube"),
            ]:
                content = news_item.get(post_key)
                if isinstance(content, dict):
                    if platform == "instagram":
                        md = _render_instagram_script(content)
                    elif platform == "linkedin":
                        md = _render_linkedin_post(content)
                    elif platform == "youtube":
                        md = _render_youtube_script(content)
                    else:
                        md = ""
                    
                    if md:
                        out[platform].append(
                            PostCard(title="AI News", source="Enthusiast", markdown=md)
                        )

        repos_root = enthusiasts.get("repos", {}) or {}
        if isinstance(repos_root, dict):
            for repo_name, repo_payload in repos_root.items():
                if not isinstance(repo_payload, dict):
                    continue
                for post_key, platform in [
                    ("linkedin_post", "linkedin"),
                    ("instagram_post", "instagram"),
                    ("youtube_post", "youtube"),
                ]:
                    content = repo_payload.get(post_key)
                    if isinstance(content, dict):
                        if platform == "instagram":
                            md = _render_instagram_script(content)
                        elif platform == "linkedin":
                            md = _render_linkedin_post(content)
                        elif platform == "youtube":
                            md = _render_youtube_script(content)
                        else:
                            md = ""
                        
                        if md:
                            out[platform].append(
                                PostCard(title=repo_name, source="Enthusiast", markdown=md)
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

            if platform == "instagram":
                md = _render_instagram_script(t)
            elif platform == "linkedin":
                md = _render_linkedin_post(t)
            elif platform == "medium":
                md = _render_medium_article(t)
            elif platform == "youtube":
                md = _render_youtube_script(t)
            else:
                md = ""

            if md:
                title = t.get("title") or "Fundamentals"
                out[platform].append(
                    PostCard(title=str(title), source="Teacher", markdown=md)
                )

    return out


def _render_linkedin_post(data: Dict[str, Any]) -> str:
    """Helper to render LinkedInPost model into markdown."""
    parts = []
    
    hook = data.get("hook")
    if hook:
        parts.append(f"{hook}\n")
    
    context = data.get("context")
    if context:
        parts.append(f"{context}\n")
        
    insight = data.get("insight")
    if insight:
        parts.append(f"{insight}\n")
        
    takeaways = data.get("key_takeaways", [])
    if isinstance(takeaways, list) and takeaways:
        parts.append("Key Takeaways:")
        for t in takeaways:
            parts.append(f"- {t}")
        parts.append("")
            
    thought = data.get("closing_thought")
    if thought:
        parts.append(f"{thought}\n")
        
    cta = data.get("call_to_action")
    if cta:
        parts.append(f"{cta}\n")
        
    hashtags = data.get("hashtags")
    if isinstance(hashtags, list):
        parts.append(" ".join(hashtags))
    elif isinstance(hashtags, str):
        parts.append(hashtags)
        
    return "\n".join(parts).strip()


def _render_medium_article(data: Dict[str, Any]) -> str:
    """Helper to render MediumArticle model into markdown."""
    parts = []
    
    title = data.get("title")
    if title:
        parts.append(f"# {title}\n")
        
    intro = data.get("introduction")
    if intro:
        parts.append(f"{intro}\n")
        
    bg = data.get("background")
    if bg:
        parts.append(f"## Background\n{bg}\n")
        
    explanation = data.get("main_explanation")
    if explanation:
        parts.append(f"## Deep Dive\n{explanation}\n")
        
    cases = data.get("examples_or_use_cases", [])
    if isinstance(cases, list) and cases:
        parts.append("## Use Cases & Examples")
        for c in cases:
            parts.append(f"- {c}")
        parts.append("")
        
    insights = data.get("key_insights", [])
    if isinstance(insights, list) and insights:
        parts.append("## Key Insights")
        for i in insights:
            parts.append(f"- {i}")
        parts.append("")
        
    future = data.get("future_implications")
    if future:
        parts.append(f"## Future Outlook\n{future}\n")
        
    conclusion = data.get("conclusion")
    if conclusion:
        parts.append(f"## Conclusion\n{conclusion}")
        
    return "\n".join(parts).strip()


def _render_youtube_script(data: Dict[str, Any]) -> str:
    """Helper to render YouTubeScript model into markdown."""
    parts = []
    
    title = data.get("title")
    if title:
        parts.append(f"# YouTube Script: {title}")
        
    duration = data.get("target_duration_minutes")
    if duration:
        parts.append(f"*Target Duration: {duration} minutes*\n")
        
    segments = data.get("segments", [])
    if isinstance(segments, list):
        for seg in segments:
            if not isinstance(seg, dict):
                continue
            
            s_type = seg.get("segment_type", "").upper()
            s_title = seg.get("title", "")
            narration = seg.get("narration", "")
            points = seg.get("key_points", [])
            s_duration = seg.get("estimated_duration_seconds", "?")
            
            parts.append(f"## [{s_type}] {s_title} ({s_duration}s)")
            parts.append(f"{narration}\n")
            
            if isinstance(points, list) and points:
                parts.append("**Key Points:**")
                for p in points:
                    parts.append(f"- {p}")
                parts.append("")
                
    return "\n".join(parts).strip()


def _render_instagram_script(data: Dict[str, Any]) -> str:
    """Helper to render ReelScript model into markdown."""
    parts = []
    
    title = data.get("title")
    if title:
        parts.append(f"# Instagram Reel: {title}\n")
    
    scenes = data.get("scenes", [])
    if isinstance(scenes, list):
        for scene in scenes:
            if not isinstance(scene, dict):
                continue
            
            s_num = scene.get("scene_number", "?")
            s_type = str(scene.get("scene_type", "")).replace("_", " ").title()
            duration = scene.get("duration_seconds", "?")
            script = scene.get("script", "")
            angle = str(scene.get("camera_angle", "")).replace("_", " ").title()
            shot = str(scene.get("shot_type", "")).replace("_", " ").title()
            
            parts.append(f"## Scene {s_num}: {s_type} ({duration}s)")
            parts.append(f"**Camera:** {angle} | **Shot:** {shot}")
            parts.append(f"> {script}")
            
            visual_cues = scene.get("visual_cues", [])
            if isinstance(visual_cues, list) and visual_cues:
                parts.append("\n**Visual Cues:**")
                for cue in visual_cues:
                    if not isinstance(cue, dict): continue
                    text = cue.get("text_overlay")
                    anim = cue.get("animation")
                    icon = cue.get("icon")
                    
                    cue_parts = []
                    if text: cue_parts.append(f"Text: {text}")
                    if anim: cue_parts.append(f"Anim: {anim}")
                    if icon: cue_parts.append(f"Icon: {icon}")
                    if cue_parts:
                        parts.append(f"- {' | '.join(cue_parts)}")
            parts.append("")

    total_duration = data.get("total_duration_seconds")
    if total_duration:
        parts.append(f"**Total Duration:** {total_duration}s")
        
    return "\n".join(parts).strip()

