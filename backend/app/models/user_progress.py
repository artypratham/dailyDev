import uuid
from datetime import datetime, date
from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    streak_count = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(Date, nullable=True)
    total_concepts_learned = Column(Integer, default=0)
    total_articles_read = Column(Integer, default=0)
    badges = Column(JSONB, default=[])  # ["7-day-streak", "topic-master", etc.]
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint
    __table_args__ = (
        UniqueConstraint("user_id", "topic_id", name="unique_user_progress"),
    )

    # Relationships
    user = relationship("User", back_populates="progress")
    topic = relationship("Topic", back_populates="progress")

    def __repr__(self):
        return f"<UserProgress user_id={self.user_id} streak={self.streak_count}>"
