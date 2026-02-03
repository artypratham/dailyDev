from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID


class RoadmapItemResponse(BaseModel):
    """Schema for a single roadmap item."""
    id: UUID
    day_number: int
    concept_title: str
    concept_slug: str
    difficulty: str
    estimated_read_time: int
    status: str
    scheduled_date: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    responded_at: Optional[datetime] = None
    has_article: bool = False

    class Config:
        from_attributes = True


class RoadmapResponse(BaseModel):
    """Schema for complete roadmap response."""
    topic_id: UUID
    topic_name: str
    total_days: int
    completed_days: int
    current_day: int
    items: List[RoadmapItemResponse]

    class Config:
        from_attributes = True
