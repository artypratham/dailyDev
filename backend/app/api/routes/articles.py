from typing import List, Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.topic import Topic
from app.models.roadmap import Roadmap
from app.models.article import Article
from app.models.saved_article import SavedArticle
from app.models.user_progress import UserProgress
from app.schemas.article import ArticleResponse, ArticleSave
from app.services.llm_service import llm_service

router = APIRouter()


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific article by ID."""
    result = await db.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )

    # Increment view count
    article.view_count += 1

    # Get roadmap and topic info
    roadmap = await db.get(Roadmap, article.roadmap_id)
    topic = await db.get(Topic, roadmap.topic_id) if roadmap else None

    # Check if saved by current user
    result = await db.execute(
        select(SavedArticle).where(
            and_(
                SavedArticle.user_id == current_user.id,
                SavedArticle.article_id == article_id
            )
        )
    )
    saved = result.scalar_one_or_none()

    # Update user progress if this is their roadmap
    if roadmap and roadmap.user_id == current_user.id:
        if roadmap.status != "read":
            roadmap.status = "read"
            roadmap.responded_at = datetime.utcnow()

            # Update progress
            result = await db.execute(
                select(UserProgress).where(
                    and_(
                        UserProgress.user_id == current_user.id,
                        UserProgress.topic_id == roadmap.topic_id
                    )
                )
            )
            progress = result.scalar_one_or_none()
            if progress:
                progress.total_articles_read += 1
                progress.total_concepts_learned += 1

                # Update streak
                today = date.today()
                if progress.last_activity_date:
                    days_diff = (today - progress.last_activity_date).days
                    if days_diff == 1:
                        progress.streak_count += 1
                    elif days_diff > 1:
                        progress.streak_count = 1
                else:
                    progress.streak_count = 1

                progress.last_activity_date = today
                progress.longest_streak = max(
                    progress.longest_streak,
                    progress.streak_count
                )

                # Award badges
                if not progress.badges:
                    progress.badges = []
                if progress.streak_count >= 7 and "7-day-streak" not in progress.badges:
                    progress.badges = progress.badges + ["7-day-streak"]
                if progress.streak_count >= 30 and "30-day-streak" not in progress.badges:
                    progress.badges = progress.badges + ["30-day-streak"]

    await db.commit()
    await db.refresh(article)

    return ArticleResponse(
        id=article.id,
        title=article.title,
        slug=article.slug,
        eli5_content=article.eli5_content,
        technical_content=article.technical_content,
        code_snippets=article.code_snippets,
        real_world_examples=article.real_world_examples,
        practice_problems=article.practice_problems,
        tags=article.tags,
        view_count=article.view_count,
        avg_read_time=article.avg_read_time,
        created_at=article.created_at,
        is_saved=saved is not None,
        user_notes=saved.notes if saved else None,
        topic_name=topic.name if topic else None,
        day_number=roadmap.day_number if roadmap else None,
        difficulty=roadmap.difficulty if roadmap else None,
    )


@router.post("/{article_id}/generate")
async def generate_article(
    article_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate article content for a roadmap item (on-demand)."""
    # Find the roadmap item
    result = await db.execute(select(Roadmap).where(Roadmap.id == article_id))
    roadmap = result.scalar_one_or_none()

    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap item not found"
        )

    # Check if article already exists
    result = await db.execute(
        select(Article).where(Article.roadmap_id == roadmap.id)
    )
    existing_article = result.scalar_one_or_none()
    if existing_article:
        return {"article_id": str(existing_article.id), "message": "Article already exists"}

    # Get topic
    topic = await db.get(Topic, roadmap.topic_id)

    # Generate article content
    article_content = await llm_service.generate_article(
        topic_name=topic.name if topic else "Interview Prep",
        concept_name=roadmap.concept_title,
        user_skill_summary=str(current_user.skill_analysis) if current_user.skill_analysis else None
    )

    # Create article
    article = Article(
        roadmap_id=roadmap.id,
        title=roadmap.concept_title,
        slug=roadmap.concept_slug,
        eli5_content=article_content.get("eli5", ""),
        technical_content=article_content.get("technical", ""),
        code_snippets=article_content.get("code_snippets", []),
        real_world_examples=article_content.get("real_world", ""),
        practice_problems=article_content.get("practice", []),
    )
    db.add(article)
    await db.commit()
    await db.refresh(article)

    return {"article_id": str(article.id), "message": "Article generated successfully"}


@router.post("/{article_id}/save")
async def save_article(
    article_id: str,
    save_data: ArticleSave,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Save an article to user's library."""
    # Verify article exists
    result = await db.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )

    # Check if already saved
    result = await db.execute(
        select(SavedArticle).where(
            and_(
                SavedArticle.user_id == current_user.id,
                SavedArticle.article_id == article_id
            )
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        # Update notes
        existing.notes = save_data.notes
    else:
        # Create new saved article
        saved = SavedArticle(
            user_id=current_user.id,
            article_id=article_id,
            notes=save_data.notes,
        )
        db.add(saved)

    await db.commit()
    return {"message": "Article saved successfully"}


@router.delete("/{article_id}/save")
async def unsave_article(
    article_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove article from user's library."""
    result = await db.execute(
        select(SavedArticle).where(
            and_(
                SavedArticle.user_id == current_user.id,
                SavedArticle.article_id == article_id
            )
        )
    )
    saved = result.scalar_one_or_none()

    if saved:
        await db.delete(saved)
        await db.commit()

    return {"message": "Article removed from library"}


@router.get("/library/saved")
async def get_saved_articles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's saved articles."""
    result = await db.execute(
        select(SavedArticle).where(
            SavedArticle.user_id == current_user.id
        ).order_by(SavedArticle.saved_at.desc())
    )
    saved_articles = result.scalars().all()

    articles_data = []
    for saved in saved_articles:
        article = await db.get(Article, saved.article_id)
        if not article:
            continue

        roadmap = await db.get(Roadmap, article.roadmap_id)
        topic = await db.get(Topic, roadmap.topic_id) if roadmap else None

        articles_data.append({
            "id": str(article.id),
            "title": article.title,
            "slug": article.slug,
            "topic_name": topic.name if topic else "Unknown",
            "day_number": roadmap.day_number if roadmap else None,
            "difficulty": roadmap.difficulty if roadmap else None,
            "avg_read_time": article.avg_read_time,
            "tags": article.tags,
            "saved_at": saved.saved_at.isoformat(),
            "notes": saved.notes,
        })

    return articles_data
