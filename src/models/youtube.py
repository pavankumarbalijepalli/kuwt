from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class SegmentType(str, Enum):
    HOOK = "hook"
    INTRO = "intro"
    PROBLEM = "problem"
    EXPLANATION = "explanation"
    BREAKDOWN = "breakdown"
    EXAMPLE = "example"
    TAKEAWAY = "takeaway"
    OUTRO = "outro"
    CTA = "call_to_action"


class YouTubeSegment(BaseModel):
    segment_type: SegmentType = Field(
        ..., description="Narrative role of the segment"
    )

    title: str = Field(
        ..., description="Short title describing this segment"
    )

    narration: str = Field(
        ..., description="Spoken script for this segment"
    )

    key_points: List[str] = Field(
        default_factory=list,
        description="Important bullet points covered in this segment"
    )

    estimated_duration_seconds: int = Field(
        ..., description="Approximate duration of this segment"
    )


class YouTubeScript(BaseModel):
    title: str = Field(
        ..., description="Video title"
    )

    target_duration_minutes: int = Field(
        ..., description="Expected total video duration"
    )

    segments: List[YouTubeSegment] = Field(
        ..., description="Ordered segments that form the full video"
    )