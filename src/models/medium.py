from pydantic import BaseModel, Field
from typing import List


class MediumArticle(BaseModel):
    title: str = Field(
        ..., description="Compelling article title"
    )

    introduction: str = Field(
        ..., description="Introduction explaining the topic and why it matters"
    )

    background: str = Field(
        ..., description="Background context needed to understand the topic"
    )

    main_explanation: str = Field(
        ..., description="Detailed explanation of the tool, concept, or idea"
    )

    examples_or_use_cases: List[str] = Field(
        ..., description="Real-world use cases or examples"
    )

    key_insights: List[str] = Field(
        ..., description="Key lessons or takeaways from the article"
    )

    future_implications: str = Field(
        ..., description="Discussion of future trends or impact"
    )

    conclusion: str = Field(
        ..., description="Final summary and takeaway"
    )