from pydantic import BaseModel, Field
from typing import List, Optional


class Content(BaseModel):
    title: str = Field(
        ...,
        description="Heading of the section (internal use, not required in final output).",
    )
    content: str = Field(..., description="Content of the section.")


class LinkedInResearchPost(BaseModel):
    hook: Content = Field(..., description="1–2 sentence hook that grabs attention.")
    research_problem: Content = Field(
        ..., description="Short explanation of the research problem and why it matters."
    )
    key_insights: List[str] = Field(
        ...,
        description="3–5 punchy bullet points summarizing main insights or findings.",
    )
    why_it_matters: Content = Field(
        ..., description="2–3 sentences explaining real-world impact or significance."
    )
    closing_reflection: Content = Field(
        ..., description="A short takeaway or reflective closing statement/question."
    )
    word_count: int = Field(
        ..., description="Total word count (should be below 130)."
    )
    relavant_hashtags: str = Field(
        ..., description="5–7 relevant hashtags for the LinkedIn post."
    )


class MediumResearchArticle(BaseModel):
    hook_opening: Content = Field(
        ...,
        description="Compelling hook such as a question, scenario, bold statement, or surprising fact.",
    )
    research_problem: Content = Field(
        ...,
        description="Explanation of the problem the researchers tackled and why it matters.",
    )
    background_context: Content = Field(
        ...,
        description="Essential background, analogies, examples, and prior limitations (if any).",
    )
    core_ideas_methodology: Content = Field(
        ...,
        description="Simplified explanation of the core concepts, assumptions, and methods used.",
    )
    key_findings: Content = Field(
        ...,
        description="Major results, discoveries, and simplified metrics or comparisons.",
    )
    real_world_impact: Content = Field(
        ..., description="Why these results matter, applications, and future potential."
    )
    limitations_future_work: Content = Field(
        ...,
        description="Limitations acknowledged by researchers and areas for future study.",
    )
    closing_reflection: Content = Field(
        ..., description="Thoughtful concluding statement or call for reflection."
    )

    word_count: Optional[int] = Field(
        None,
        description="Total word count of the generated article (target: 800–1200).",
    )
    relavant_hashtags: str = Field(
        ..., description="5–7 relevant hashtags for the Medium article."
    )
    suggested_image_description: str = Field(
        ...,
        description="A brief description of a suggested image to accompany the article.",
    )


class YouTubeResearchScript(BaseModel):
    hook: Content = Field(
        ...,
        description="A 20–30 second hook that grabs attention with a scenario, stat, or question.",
    )
    intro: Content = Field(
        ..., description="A brief intro that frames the video, topic, and expectations."
    )
    research_problem: Content = Field(
        ..., description="Explanation of the research problem and why it matters."
    )
    background_setup: Content = Field(
        ...,
        description="Accessible background, examples, and context to understand the topic.",
    )
    core_ideas_methodology: Content = Field(
        ...,
        description="Simplified explanation of the research methods, logic, and core ideas.",
    )
    key_findings: Content = Field(
        ..., description="Narrative breakdown of important discoveries or results."
    )
    real_world_implications: Content = Field(
        ...,
        description="Explanation of industry, societal, or future impact of the research.",
    )
    limitations_future_work: Content = Field(
        ...,
        description="Short section about limitations and potential future research directions.",
    )
    closing: Content = Field(
        ..., description="A concluding reflection, takeaway, or call to action."
    )
    word_count: int = Field(
        ...,
        description="Total script length; target is roughly 1000–1300 words for an ~8-minute video.",
    )
    seo_tags: str = Field(
        ..., description="5–7 relevant SEO keywords for the YouTube video."
    )
    hashtags: str = Field(
        ..., description="5–7 appropriate hashtags for the YouTube video."
    )
    creator_tips: str = Field(
        ...,
        description="Suggestions for visuals, tone, and pacing to enhance viewer engagement.",
    )


class InstagramResearchScript(BaseModel):
    hook: Content = Field(
        ...,
        description="A 20–30 second hook that grabs attention with a scenario, stat, or question.",
    )
    intro: Content = Field(
        ..., description="A brief intro that frames the video, topic, and expectations."
    )
    research_problem: Content = Field(
        ..., description="Explanation of the research problem and why it matters."
    )
    background_setup: Content = Field(
        ...,
        description="Accessible background, examples, and context to understand the topic.",
    )
    core_ideas_methodology: Content = Field(
        ...,
        description="Simplified explanation of the research methods, logic, and core ideas.",
    )
    key_findings: Content = Field(
        ..., description="Narrative breakdown of important discoveries or results."
    )
    real_world_implications: Content = Field(
        ...,
        description="Explanation of industry, societal, or future impact of the research.",
    )
    limitations_future_work: Content = Field(
        ...,
        description="Short section about limitations and potential future research directions.",
    )
    closing: Content = Field(
        ..., description="A concluding reflection, takeaway, or call to action."
    )
    word_count: int = Field(
        ...,
        description="Total script length; target is roughly 1000–1300 words for an ~8-minute video.",
    )
    seo_tags: str = Field(
        ..., description="5–7 relevant SEO keywords for the YouTube video."
    )
    hashtags: str = Field(
        ..., description="5–7 appropriate hashtags for the YouTube video."
    )
    creator_tips: str = Field(
        ...,
        description="Suggestions for visuals, tone, and pacing to enhance viewer engagement.",
    )


class ResearchersResponse(BaseModel):
    linkedin_post: LinkedInResearchPost = Field(
        ..., description="Content for LinkedIn post."
    )
    instagram_post: InstagramResearchScript = Field(
        ..., description="Content for Instagram post."
    )
    medium_post: MediumResearchArticle = Field(
        ..., description="Content for Medium article."
    )
    youtube_post: YouTubeResearchScript = Field(
        ..., description="Content for YouTube video."
    )
