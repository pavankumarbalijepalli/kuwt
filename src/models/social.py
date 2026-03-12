from pydantic import BaseModel
from typing import Optional
from models.linkedin import LinkedInPost
from models.instagram import ReelScript
from models.medium import MediumArticle
from models.youtube import YouTubeScript

class SocialMediaResponse(BaseModel):
    linkedin_post: LinkedInPost
    instagram_post: ReelScript
    medium_post: Optional[MediumArticle] = None
    youtube_post: YouTubeScript
