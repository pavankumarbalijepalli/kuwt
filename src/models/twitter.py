from pydantic import BaseModel, Field
from typing import List


class TwitterPost(BaseModel):
    content: str = Field(..., description="The content of the tweet, max 280 characters")

class TwitterThread(BaseModel):
    title: str = Field(..., description="Title or summary of the thread")
    posts: List[TwitterPost] = Field(..., description="List of tweets in the thread")
