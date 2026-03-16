from pydantic import BaseModel
from typing import Optional
from models.linkedin import LinkedInPost
from models.instagram import ReelScript
from models.twitter import TwitterThread
from models.youtube import YouTubeScript

class SocialMediaResponse(BaseModel):
    linkedin_post: LinkedInPost
    instagram_post: ReelScript
    twitter_post: Optional[TwitterThread] = None
    youtube_post: YouTubeScript
