import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roadmap_id = Column(UUID(as_uuid=True), ForeignKey("roadmap.id"), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    eli5_content = Column(Text, nullable=True)  # ELI5 explanation
    technical_content = Column(Text, nullable=True)  # Technical deep dive
    code_snippets = Column(JSONB, nullable=True)  # [{language, code, explanation}]
    real_world_examples = Column(Text, nullable=True)
    practice_problems = Column(JSONB, nullable=True)  # [{question, difficulty, link}]
    tags = Column(JSONB, nullable=True)  # ["arrays", "hashing", "optimization"]
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    view_count = Column(Integer, default=0)
    avg_read_time = Column(Integer, default=10)  # minutes

    # Relationships
    roadmap = relationship("Roadmap", back_populates="article")
    saved_by = relationship("SavedArticle", back_populates="article")

    def __repr__(self):
        return f"<Article {self.title}>"
