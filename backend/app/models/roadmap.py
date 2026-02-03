import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Roadmap(Base):
    __tablename__ = "roadmap"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    concept_title = Column(String(255), nullable=False)
    concept_slug = Column(String(255), nullable=False)
    hook_message = Column(Text, nullable=True)
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    estimated_read_time = Column(Integer, default=10)  # minutes
    scheduled_date = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    responded_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="pending")  # pending, sent, read, skipped
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="roadmaps")
    topic = relationship("Topic", back_populates="roadmaps")
    article = relationship("Article", back_populates="roadmap", uselist=False)

    def __repr__(self):
        return f"<Roadmap day={self.day_number} concept={self.concept_title}>"
