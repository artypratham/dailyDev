import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  # Emoji or icon name
    difficulty_levels = Column(JSONB, default=["easy", "medium", "hard"])
    total_concepts = Column(String(10), default="30")  # Number of concepts in topic
    is_active = Column(String(10), default="true")

    # Relationships
    user_topics = relationship("UserTopic", back_populates="topic")
    roadmaps = relationship("Roadmap", back_populates="topic")
    progress = relationship("UserProgress", back_populates="topic")

    def __repr__(self):
        return f"<Topic {self.name}>"
