from pydantic import BaseModel, Field

class LinkedinNewsPost(BaseModel):
    hook: str = Field(..., description="Engaging opening line to capture attention")
    content: str = Field(..., description="Main body content of the post")
    call_to_action: str = Field(..., description="CTA to encourage engagement")
    hashtags: list[str] = Field(default_factory=list, description="Relevant hashtags")
    engagement_tips: str = Field(..., description="Tips for maximizing engagement")

class MediumNewsPost(BaseModel):
    headline: str = Field(..., description="Compelling article headline")
    hook: str = Field(..., description="Opening paragraph to hook readers")
    what_happened: str = Field(..., description="Detailed explanation of the news or tool")
    what_will_change: str = Field(..., description="Analysis of how this will impact the industry or users")
    who_will_be_affected: str = Field(..., description="Discussion of who will be affected and how")
    key_takeaways: list[str] = Field(
        ..., description="Main points readers should remember"
    )
    whats_next: str = Field(..., description="Discussion of potential future developments or implications")
    conclusion: str = Field(..., description="Summary and final thoughts")
    seo_tags: list[str] = Field(default_factory=list, description="SEO keywords for the article")
    hashtags: list[str] = Field(default_factory=list, description="Relevant hashtags for the article")
    suggested_image_description: str = Field(..., description="Description for a suggested accompanying image for the article")
    call_to_action: str = Field(..., description="Next steps or engagement prompt")

class YoutubeNewsVideo(BaseModel):
    title: str = Field(..., description="Video title optimized for search and clicks")
    hook: str = Field(..., description="First 10 seconds script to retain viewers")
    what_happened: str = Field(..., description="Detailed explanation of the news or tool")
    what_will_change: str = Field(..., description="Analysis of how this will impact the industry or users")
    who_will_be_affected: str = Field(..., description="Discussion of who will be affected and how")
    key_takeaways: list[str] = Field(
        ..., description="Main points readers should remember"
    )
    whats_next: str = Field(..., description="Discussion of potential future developments or implications")
    thumbnailText: str = Field(..., description="Text for thumbnail")
    tags: list[str] = Field(..., description="SEO tags")
    call_to_action: str = Field(..., description="Subscribe/engagement prompt")

class InstagramNewsVideo(BaseModel):
    caption: str = Field(..., description="Engaging post caption with hook")
    hook: str = Field(..., description="First 3 seconds hook for video")
    content: str = Field(..., description="Video content description")
    hashtags: list[str] = Field(..., description="Instagram hashtags")
    call_to_action: str = Field(..., description="Engagement prompt")
    emoji_strategy: str = Field(..., description="Emoji use for visual appeal")