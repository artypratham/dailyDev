from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.topic import Topic
from app.models.roadmap import Roadmap
from app.models.article import Article
from app.schemas.roadmap import RoadmapResponse, RoadmapItemResponse

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_all_roadmaps(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all roadmaps for current user."""
    # Get unique topic IDs for user's roadmaps
    result = await db.execute(
        select(Roadmap.topic_id).where(
            Roadmap.user_id == current_user.id
        ).distinct()
    )
    topic_ids = [row[0] for row in result.all()]

    roadmaps_data = []
    for topic_id in topic_ids:
        topic = await db.get(Topic, topic_id)
        if not topic:
            continue

        result = await db.execute(
            select(Roadmap).where(
                and_(
                    Roadmap.user_id == current_user.id,
                    Roadmap.topic_id == topic_id
                )
            ).order_by(Roadmap.day_number)
        )
        items = result.scalars().all()

        completed = len([i for i in items if i.status == "read"])
        current_day = next(
            (i.day_number for i in items if i.status in ["pending", "sent"]),
            len(items)
        )

        roadmaps_data.append({
            "topic_id": str(topic_id),
            "topic_name": topic.name,
            "topic_slug": topic.slug,
            "total_days": len(items),
            "completed_days": completed,
            "current_day": current_day,
        })

    return roadmaps_data


@router.get("/topic/{topic_id}")
async def get_roadmap_by_topic(
    topic_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed roadmap for a specific topic."""
    topic = await db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )

    result = await db.execute(
        select(Roadmap).where(
            and_(
                Roadmap.user_id == current_user.id,
                Roadmap.topic_id == topic_id
            )
        ).order_by(Roadmap.day_number)
    )
    items = result.scalars().all()

    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No roadmap found for this topic"
        )

    # Check which items have articles
    items_data = []
    for item in items:
        result = await db.execute(
            select(Article).where(Article.roadmap_id == item.id)
        )
        article = result.scalar_one_or_none()

        items_data.append({
            "id": str(item.id),
            "day_number": item.day_number,
            "concept_title": item.concept_title,
            "concept_slug": item.concept_slug,
            "difficulty": item.difficulty,
            "estimated_read_time": item.estimated_read_time,
            "status": item.status,
            "scheduled_date": item.scheduled_date.isoformat() if item.scheduled_date else None,
            "sent_at": item.sent_at.isoformat() if item.sent_at else None,
            "responded_at": item.responded_at.isoformat() if item.responded_at else None,
            "has_article": article is not None,
            "article_id": str(article.id) if article else None,
        })

    completed = len([i for i in items if i.status == "read"])
    current_day = next(
        (i.day_number for i in items if i.status in ["pending", "sent"]),
        len(items)
    )

    return {
        "topic_id": str(topic_id),
        "topic_name": topic.name,
        "total_days": len(items),
        "completed_days": completed,
        "current_day": current_day,
        "items": items_data,
    }


@router.get("/today")
async def get_today_concept(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get today's concept for the user."""
    # Find the next pending or sent concept
    result = await db.execute(
        select(Roadmap).where(
            and_(
                Roadmap.user_id == current_user.id,
                Roadmap.status.in_(["pending", "sent"])
            )
        ).order_by(Roadmap.day_number)
    )
    roadmap_item = result.scalar_one_or_none()

    if not roadmap_item:
        return {"message": "No concepts scheduled for today"}

    topic = await db.get(Topic, roadmap_item.topic_id)

    # Check if article exists
    result = await db.execute(
        select(Article).where(Article.roadmap_id == roadmap_item.id)
    )
    article = result.scalar_one_or_none()

    return {
        "id": str(roadmap_item.id),
        "topic_name": topic.name if topic else "Unknown",
        "day_number": roadmap_item.day_number,
        "concept_title": roadmap_item.concept_title,
        "concept_slug": roadmap_item.concept_slug,
        "difficulty": roadmap_item.difficulty,
        "estimated_read_time": roadmap_item.estimated_read_time,
        "hook_message": roadmap_item.hook_message,
        "status": roadmap_item.status,
        "has_article": article is not None,
        "article_id": str(article.id) if article else None,
    }
