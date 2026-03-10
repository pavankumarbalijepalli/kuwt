from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

Platform = Literal["linkedin", "instagram", "medium", "youtube"]


@dataclass(frozen=True)
class PostCard:
    title: str
    source: str
    markdown: str


@dataclass(frozen=True)
class PlatformPost:
    platform: Platform
    date: str
    cards: Sequence[PostCard]

