from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class CameraAngle(str, Enum):
    CLOSE_UP = "close_up"
    MEDIUM = "medium"
    WIDE = "wide"
    SIDE_ANGLE = "side_angle"
    LOW_ANGLE = "low_angle"
    HIGH_ANGLE = "high_angle"


class ShotType(str, Enum):
    STATIC = "static"
    PUSH_IN = "push_in"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    HANDHELD = "handheld"


class SceneType(str, Enum):
    HOOK = "hook"
    CONTEXT = "context"
    TENSION = "tension"
    PIVOT = "pivot"
    PAYOFF = "payoff"
    CTA = "call_to_action"

class VisualCue(BaseModel):
    icon: Optional[str] = None
    image: Optional[str] = None
    clip: Optional[str] = None


class Scene(BaseModel):
    scene_number: int = Field(..., description="Sequential scene number")
    scene_type: SceneType = Field(..., description="Narrative role of the scene")
    duration_seconds: float = Field(..., description="Length of the scene")

    script: str = Field(..., description="Exact words the creator should say")

    camera_angle: CameraAngle = Field(
        ..., description="Camera framing used in the shot"
    )

    shot_type: ShotType = Field(
        default=ShotType.STATIC,
        description="Camera motion or style"
    )

    visual_cues: List[VisualCue] = Field(
        default=None,
        description="Suggestions for visual elements such as images, icons, or quick clips to make the scene more engaging"
    )


class ReelScript(BaseModel):
    title: Optional[str] = None
    total_duration_seconds: Optional[float] = None
    hook_scene: Scene = Field(..., description="Hook scene")
    context_scene: Scene = Field(..., description="Context scene")
    tension_scene: Scene = Field(..., description="Tension scene")
    pivot_scene: Scene = Field(..., description="Pivot scene")
    payoff_scene: Scene = Field(..., description="Payoff scene")
    cta_scene: Scene = Field(..., description="Call to action scene")