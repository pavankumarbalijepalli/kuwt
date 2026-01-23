from pydantic import BaseModel, Field
from typing import List, Optional

class HeadingsOutput(BaseModel):
    main_headings: List[str] = Field(
        ..., description="A list of all Headings from the content."
    )

class LinkedInSection(BaseModel):
    title: str = Field(..., description="Heading of the section (internal use, not required in final output).")
    content: str = Field(..., description="Content of the section.")

class LinkedInResearchPost(BaseModel):
    hook: LinkedInSection = Field(
        ..., 
        description="1–2 sentence hook that grabs attention."
    )
    research_problem: LinkedInSection = Field(
        ..., 
        description="Short explanation of the research problem and why it matters."
    )
    key_insights: List[str] = Field(
        ..., 
        description="3–5 punchy bullet points summarizing main insights or findings."
    )
    why_it_matters: LinkedInSection = Field(
        ..., 
        description="2–3 sentences explaining real-world impact or significance."
    )
    closing_reflection: LinkedInSection = Field(
        ..., 
        description="A short takeaway or reflective closing statement/question."
    )
    word_count: int = Field(
        ..., 
        description="Total word count (should be between 120–220)."
    )
    relavant_hashtags: str = Field(
        ...,
        description="5–7 relevant hashtags for the LinkedIn post."
    )
    
class ArticleSection(BaseModel):
    title: str = Field(..., description="The heading of the section.")
    content: str = Field(..., description="The main text of the section, paraphrased and simplified.")

class MediumResearchArticle(BaseModel):
    hook_opening: ArticleSection = Field(
        ..., 
        description="Compelling hook such as a question, scenario, bold statement, or surprising fact."
    )
    research_problem: ArticleSection = Field(
        ..., 
        description="Explanation of the problem the researchers tackled and why it matters."
    )
    background_context: ArticleSection = Field(
        ..., 
        description="Essential background, analogies, examples, and prior limitations (if any)."
    )
    core_ideas_methodology: ArticleSection = Field(
        ..., 
        description="Simplified explanation of the core concepts, assumptions, and methods used."
    )
    key_findings: ArticleSection = Field(
        ..., 
        description="Major results, discoveries, and simplified metrics or comparisons."
    )
    real_world_impact: ArticleSection = Field(
        ..., 
        description="Why these results matter, applications, and future potential."
    )
    limitations_future_work: ArticleSection = Field(
        ..., 
        description="Limitations acknowledged by researchers and areas for future study."
    )
    closing_reflection: ArticleSection = Field(
        ..., 
        description="Thoughtful concluding statement or call for reflection."
    )

    word_count: Optional[int] = Field(
        None,
        description="Total word count of the generated article (target: 800–1200)."
    )
    relavant_hashtags: str = Field(
        ...,
        description="5–7 relevant hashtags for the Medium article."
    )
    suggested_image_description: str = Field(
        ...,
        description="A brief description of a suggested image to accompany the article."
    )
    
class YouTubeSection(BaseModel):
    title: str = Field(..., description="Internal heading for the script section.")
    content: str = Field(..., description="Narration text spoken in the video.")

class YouTubeResearchScript(BaseModel):
    hook: YouTubeSection = Field(
        ..., 
        description="A 20–30 second hook that grabs attention with a scenario, stat, or question."
    )
    intro: YouTubeSection = Field(
        ..., 
        description="A brief intro that frames the video, topic, and expectations."
    )
    research_problem: YouTubeSection = Field(
        ..., 
        description="Explanation of the research problem and why it matters."
    )
    background_setup: YouTubeSection = Field(
        ..., 
        description="Accessible background, examples, and context to understand the topic."
    )
    core_ideas_methodology: YouTubeSection = Field(
        ..., 
        description="Simplified explanation of the research methods, logic, and core ideas."
    )
    key_findings: YouTubeSection = Field(
        ..., 
        description="Narrative breakdown of important discoveries or results."
    )
    real_world_implications: YouTubeSection = Field(
        ..., 
        description="Explanation of industry, societal, or future impact of the research."
    )
    limitations_future_work: YouTubeSection = Field(
        ..., 
        description="Short section about limitations and potential future research directions."
    )
    closing: YouTubeSection = Field(
        ..., 
        description="A concluding reflection, takeaway, or call to action."
    )
    word_count: int = Field(
        ..., 
        description="Total script length; target is roughly 1000–1300 words for an ~8-minute video."
    )
    seo_tags: str = Field(
        ...,
        description="5–7 relevant SEO keywords for the YouTube video."
    )
    hashtags: str = Field(
        ...,
        description="5–7 appropriate hashtags for the YouTube video."
    )
    creator_tips: str = Field(
        ...,
        description="Suggestions for visuals, tone, and pacing to enhance viewer engagement."
    )