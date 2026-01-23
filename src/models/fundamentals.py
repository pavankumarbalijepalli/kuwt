from pydantic import BaseModel, Field
from typing import List, Literal, Dict

class YoutubeResponse(BaseModel):
    title: str = Field(
        ..., 
        description="Video title")
    hook: str = Field(
        ..., 
        description="Hook section: Start with real-world scenario or question to grab attention")
    intuition: str = Field(
        ..., 
        description="High-level mental model or analogy explaining the concept which follows the hook example"
    )
    technical_details: str = Field(
        ..., 
        description=(
            "Unified section containing: explanation, step-wise example, "
            "when to use, and limitations/misconceptions"
            "must follow intiution section"
        )
    )
    cta: str = Field(
        ..., 
        description="Wrap-up, summary, and call to action + pointer to next topics"
    )
    seo_tags: str = Field(
        ...,
        description="5–7 relevant SEO keywords for the YouTube video."
    )
    hashtags: str = Field(
        ...,
        description="5–7 appropriate hashtags for the YouTube video."
    )
    walkthrough_code: str = Field(
        ...,
        description="A python file that contains code snippets separated by comments for walkthrough purposes. Mandatory!"
    )
    
class MediumResponse(BaseModel):
    title: str = Field(
        ..., 
        description="Engaging title for the Medium article."
    )
    introduction: str = Field(
        ..., 
        description="A compelling introduction that hooks the reader."
    )
    body: str = Field(
        ..., 
        description="Unified section containing: explanation, step-wise example, "
            "when to use, and limitations/misconceptions"
            "must follow intuition section"
            "Total of 800 words."
    )
    conclusion: str = Field(
        ..., 
        description="A concise conclusion that summarizes key points and provides a call to action."
    )
    seo_tags: str = Field(
        ...,
        description="5–7 relevant SEO keywords for the Medium article."
    )
    hashtags: str = Field(
        ...,
        description="5–7 relevant hashtags for the Medium article."
    )
    suggested_image_description: str = Field(
        ...,
        description="A brief description of a suggested image to accompany the article."
    )
    
class LinkedinResponse(BaseModel):
    title: str = Field(
        ..., 
        description="Engaging title for the LinkedIn article."
    )
    introduction: str = Field(
        ..., 
        description="A compelling introduction that hooks the reader."
    )
    body: str = Field(
        ..., 
        description="Unified section containing: explanation, step-wise example, "
            "when to use, and limitations/misconceptions"
            "must follow intuition section"
            "Total of 50 words."
    )
    conclusion: str = Field(
        ..., 
        description="A concise conclusion that summarizes key points and provides a call to action."
    )
    seo_tags: str = Field(
        ...,
        description="5–7 relevant SEO keywords for the LinkedIn article."
    )
    hashtags: str = Field(
        ...,
        description="5–7 relevant hashtags for the LinkedIn article."
    )
    
class InstagramResponse(BaseModel):
    hook: str = Field(
        ..., 
        description="Hook section: Start with real-world scenario or question to grab attention")
    intuition: str = Field(
        ..., 
        description="High-level mental model or analogy explaining the concept which follows the hook example"
    )
    pre_cta: str = Field(
        ..., 
        description="A brief call to action which summarizes teaching and invites them to follow or subscribe."
    )
    technical_details: str = Field(
        ..., 
        description=(
            "Unified section containing: explanation, step-wise example, "
            "when to use, and limitations/misconceptions"
            "must follow intiution section"
        )
    )
    cta: str = Field(
        ..., 
        description="Wrap-up, summary, and call to action + pointer to next topics"
    )
    caption: str = Field(
        ..., 
        description="Engaging caption for the Instagram post."
    )
    hashtags: str = Field(
        ...,
        description="5–7 relevant hashtags for the Instagram post."
    )