import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserTopic(Base):
    __tablename__ = "user_topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    start_date = Column(Date, default=date.today)
    target_completion_date = Column(Date, nullable=True)
    status = Column(String(50), default="active")  # active, paused, completed
    duration_days = Column(String(10), default="30")  # 30, 60, 90 days
    created_at = Column(DateTime, default=datetime.utcnow)

    # Unique constraint
    __table_args__ = (
        UniqueConstraint("user_id", "topic_id", name="unique_user_topic"),
    )

    # Relationships
    user = relationship("User", back_populates="user_topics")
    topic = relationship("Topic", back_populates="user_topics")

    def __repr__(self):
        return f"<UserTopic user_id={self.user_id} topic_id={self.topic_id}>"
