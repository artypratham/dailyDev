from typing import List
from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.topic import Topic
from app.models.user_topic import UserTopic
from app.models.roadmap import Roadmap
from app.models.user_progress import UserProgress
from app.schemas.topic import TopicResponse, TopicSelection
from app.services.llm_service import llm_service

router = APIRouter()


@router.get("/", response_model=List[TopicResponse])
async def get_all_topics(db: AsyncSession = Depends(get_db)):
    """Get all available topics."""
    result = await db.execute(
        select(Topic).where(Topic.is_active == "true").order_by(Topic.name)
    )
    return result.scalars().all()


@router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(topic_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific topic by ID."""
    result = await db.execute(select(Topic).where(Topic.id == topic_id))
    topic = result.scalar_one_or_none()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    return topic


@router.post("/select")
async def select_topics(
    selection: TopicSelection,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Select topics and generate personalized roadmaps."""
    if not selection.topic_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one topic must be selected"
        )

    if selection.duration_days not in [30, 60, 90]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duration must be 30, 60, or 90 days"
        )

    created_topics = []
    start_date = date.today()
    target_date = start_date + timedelta(days=selection.duration_days)

    for topic_id in selection.topic_ids:
        # Verify topic exists
        result = await db.execute(select(Topic).where(Topic.id == topic_id))
        topic = result.scalar_one_or_none()
        if not topic:
            continue

        # Check if user already has this topic
        result = await db.execute(
            select(UserTopic).where(
                UserTopic.user_id == current_user.id,
                UserTopic.topic_id == topic_id
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            continue  # Skip if already selected

        # Create user-topic association
        user_topic = UserTopic(
            user_id=current_user.id,
            topic_id=topic_id,
            start_date=start_date,
            target_completion_date=target_date,
            duration_days=str(selection.duration_days),
        )
        db.add(user_topic)

        # Create user progress record
        progress = UserProgress(
            user_id=current_user.id,
            topic_id=topic_id,
        )
        db.add(progress)

        # Generate roadmap for this topic
        roadmap_items = await llm_service.generate_roadmap(
            topic_name=topic.name,
            duration_days=selection.duration_days,
            user_level=current_user.experience_level or "intermediate"
        )

        for item in roadmap_items:
            roadmap_entry = Roadmap(
                user_id=current_user.id,
                topic_id=topic_id,
                day_number=item["day"],
                concept_title=item["concept"],
                concept_slug=item["concept"].lower().replace(" ", "-").replace("'", ""),
                difficulty=item.get("difficulty", "medium"),
                estimated_read_time=item.get("read_time", 10),
                scheduled_date=start_date + timedelta(days=item["day"] - 1),
            )
            db.add(roadmap_entry)

        created_topics.append(topic.name)

    await db.commit()

    return {
        "message": f"Successfully enrolled in {len(created_topics)} topic(s)",
        "topics": created_topics,
        "duration_days": selection.duration_days,
        "start_date": start_date.isoformat(),
        "target_date": target_date.isoformat(),
    }


@router.get("/me/selected")
async def get_my_topics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's selected topics with progress."""
    result = await db.execute(
        select(UserTopic).where(UserTopic.user_id == current_user.id)
    )
    user_topics = result.scalars().all()

    topics_data = []
    for ut in user_topics:
        # Get topic details
        topic = await db.get(Topic, ut.topic_id)
        if not topic:
            continue

        # Get progress
        result = await db.execute(
            select(UserProgress).where(
                UserProgress.user_id == current_user.id,
                UserProgress.topic_id == ut.topic_id
            )
        )
        progress = result.scalar_one_or_none()

        # Get roadmap stats
        result = await db.execute(
            select(Roadmap).where(
                Roadmap.user_id == current_user.id,
                Roadmap.topic_id == ut.topic_id
            )
        )
        roadmap_items = result.scalars().all()
        completed = len([r for r in roadmap_items if r.status == "read"])
        total = len(roadmap_items)

        topics_data.append({
            "topic_id": str(ut.topic_id),
            "topic_name": topic.name,
            "topic_slug": topic.slug,
            "topic_icon": topic.icon,
            "start_date": ut.start_date.isoformat() if ut.start_date else None,
            "target_date": ut.target_completion_date.isoformat() if ut.target_completion_date else None,
            "status": ut.status,
            "progress": {
                "completed": completed,
                "total": total,
                "percentage": round((completed / total * 100) if total > 0 else 0, 1),
                "streak": progress.streak_count if progress else 0,
            }
        })

    return topics_data
