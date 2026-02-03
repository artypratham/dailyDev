import uuid
from datetime import datetime
from sqlalchemy import Column, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class SavedArticle(Base):
    __tablename__ = "saved_articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"), nullable=False)
    notes = Column(Text, nullable=True)  # User's personal notes
    saved_at = Column(DateTime, default=datetime.utcnow)

    # Unique constraint
    __table_args__ = (
        UniqueConstraint("user_id", "article_id", name="unique_saved_article"),
    )

    # Relationships
    user = relationship("User", back_populates="saved_articles")
    article = relationship("Article", back_populates="saved_by")

    def __repr__(self):
        return f"<SavedArticle user_id={self.user_id} article_id={self.article_id}>"
