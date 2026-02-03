from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID


class TopicResponse(BaseModel):
    """Schema for topic response."""
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None
    total_concepts: str

    class Config:
        from_attributes = True


class TopicSelection(BaseModel):
    """Schema for selecting topics."""
    topic_ids: List[UUID]
    duration_days: int = 30  # 30, 60, or 90 days
