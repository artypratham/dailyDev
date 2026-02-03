import uuid
from datetime import datetime, time
from sqlalchemy import Column, String, Text, DateTime, Time
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    phone_whatsapp = Column(String(20), unique=True, nullable=True, index=True)
    name = Column(String(255), nullable=True)
    resume_url = Column(Text, nullable=True)
    skill_analysis = Column(JSONB, nullable=True)
    experience_level = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    timezone = Column(String(50), default="UTC")
    preferred_time = Column(Time, default=time(9, 0))  # 9:00 AM default
    whatsapp_connected = Column(String(50), default="pending")  # pending, connected, disconnected

    # Relationships
    user_topics = relationship("UserTopic", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("Roadmap", back_populates="user", cascade="all, delete-orphan")
    saved_articles = relationship("SavedArticle", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"
