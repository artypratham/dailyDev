from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from uuid import UUID


class CodeSnippet(BaseModel):
    """Schema for code snippet."""
    language: str
    code: str
    explanation: Optional[str] = None


class PracticeProblem(BaseModel):
    """Schema for practice problem."""
    question: str
    difficulty: str
    link: Optional[str] = None


class ArticleResponse(BaseModel):
    """Schema for article response."""
    id: UUID
    title: str
    slug: str
    eli5_content: Optional[str] = None
    technical_content: Optional[str] = None
    code_snippets: Optional[List[Dict[str, Any]]] = None
    real_world_examples: Optional[str] = None
    practice_problems: Optional[List[Dict[str, Any]]] = None
    tags: Optional[List[str]] = None
    view_count: int
    avg_read_time: int
    created_at: datetime
    is_saved: bool = False
    user_notes: Optional[str] = None

    # Related roadmap info
    topic_name: Optional[str] = None
    day_number: Optional[int] = None
    difficulty: Optional[str] = None

    class Config:
        from_attributes = True


class ArticleSave(BaseModel):
    """Schema for saving an article."""
    notes: Optional[str] = None


class ArticleListItem(BaseModel):
    """Schema for article in list view."""
    id: UUID
    title: str
    slug: str
    topic_name: str
    day_number: int
    difficulty: str
    avg_read_time: int
    tags: Optional[List[str]] = None
    is_saved: bool = False

    class Config:
        from_attributes = True
