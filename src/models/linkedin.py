from pydantic import BaseModel, Field
from typing import List


class LinkedInPost(BaseModel):
    hook: str = Field(
        ..., description="First line that grabs attention"
    )

    context: str = Field(
        ..., description="Brief explanation of the topic or event"
    )

    insight: str = Field(
        ..., description="Why this matters to professionals or developers"
    )

    key_takeaways: List[str] = Field(
        ..., description="3 to 5 important insights summarized as bullet points"
    )

    closing_thought: str = Field(
        ..., description="Forward-looking reflection or summary"
    )

    call_to_action: str = Field(
        ..., description="Encourage comments, discussion, or engagement"
    )

    hashtags: List[str] = Field(
        ..., description="Relevant hashtags for reach"
    )