from datetime import datetime, date, timedelta
from typing import List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from app.models.user import User
from app.models.roadmap import Roadmap
from app.models.article import Article
from app.services.whatsapp_service import whatsapp_service
from app.services.llm_service import llm_service
from app.core.database import async_session_maker


class SchedulerService:
    """Service for scheduling and sending daily messages."""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self._is_running = False

    def start(self):
        """Start the scheduler."""
        if not self._is_running:
            # Run every hour to check for users whose preferred time has arrived
            self.scheduler.add_job(
                self.send_daily_messages,
                CronTrigger(minute=0),  # Run at the start of every hour
                id="daily_messages",
                replace_existing=True
            )
            self.scheduler.start()
            self._is_running = True
            logger.info("Scheduler started")

    def stop(self):
        """Stop the scheduler."""
        if self._is_running:
            self.scheduler.shutdown()
            self._is_running = False
            logger.info("Scheduler stopped")

    async def send_daily_messages(self):
        """Send daily hook messages to users at their preferred time."""
        current_hour = datetime.utcnow().hour
        logger.info(f"Checking for users to send messages at hour {current_hour}")

        async with async_session_maker() as db:
            # Find users whose preferred time matches current hour
            # and who have pending roadmap items for today
            result = await db.execute(
                select(User).where(
                    and_(
                        User.whatsapp_connected == "connected",
                        User.phone_whatsapp.isnot(None)
                    )
                )
            )
            users = result.scalars().all()

            for user in users:
                # Check if user's preferred time matches current hour (UTC)
                # In production, you'd convert using user's timezone
                if user.preferred_time.hour == current_hour:
                    await self._send_user_daily_message(db, user)

    async def _send_user_daily_message(self, db: AsyncSession, user: User):
        """Send daily message to a specific user."""
        today = date.today()

        # Find next pending roadmap item for this user
        result = await db.execute(
            select(Roadmap).where(
                and_(
                    Roadmap.user_id == user.id,
                    Roadmap.status == "pending"
                )
            ).order_by(Roadmap.day_number)
        )
        roadmap_item = result.scalar_one_or_none()

        if not roadmap_item:
            logger.info(f"No pending concepts for user {user.id}")
            return

        # Check if already sent today
        if roadmap_item.sent_at and roadmap_item.sent_at.date() == today:
            logger.info(f"Already sent message to user {user.id} today")
            return

        # Generate hook message if not already generated
        if not roadmap_item.hook_message:
            topic = await db.get(roadmap_item.topic.__class__, roadmap_item.topic_id)
            hook_message = await llm_service.generate_hook_message(
                topic_name=topic.name if topic else "Interview Prep",
                concept_name=roadmap_item.concept_title,
                difficulty=roadmap_item.difficulty,
                user_experience_level=user.experience_level or "intermediate"
            )
            roadmap_item.hook_message = hook_message

        # Send WhatsApp message
        message_sid = await whatsapp_service.send_hook_message(
            to_number=user.phone_whatsapp,
            hook_message=roadmap_item.hook_message,
            concept_title=roadmap_item.concept_title
        )

        if message_sid:
            roadmap_item.sent_at = datetime.utcnow()
            roadmap_item.status = "sent"
            await db.commit()
            logger.info(f"Sent daily message to user {user.id} for concept {roadmap_item.concept_title}")
        else:
            logger.error(f"Failed to send message to user {user.id}")

    async def process_user_response(
        self,
        db: AsyncSession,
        phone_number: str,
        response: str
    ) -> bool:
        """Process user's WhatsApp response."""
        response_lower = response.strip().lower()

        # Check if response is affirmative
        if response_lower not in ["yes", "y", "yeah", "yep", "sure", "ok", "okay"]:
            return False

        # Find user by phone number
        result = await db.execute(
            select(User).where(User.phone_whatsapp == phone_number)
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.warning(f"No user found for phone {phone_number}")
            return False

        # Find the latest sent roadmap item
        result = await db.execute(
            select(Roadmap).where(
                and_(
                    Roadmap.user_id == user.id,
                    Roadmap.status == "sent"
                )
            ).order_by(Roadmap.sent_at.desc())
        )
        roadmap_item = result.scalar_one_or_none()

        if not roadmap_item:
            logger.warning(f"No sent roadmap item for user {user.id}")
            return False

        # Check if article exists, if not generate it
        result = await db.execute(
            select(Article).where(Article.roadmap_id == roadmap_item.id)
        )
        article = result.scalar_one_or_none()

        if not article:
            # Generate article
            from app.models.topic import Topic
            topic = await db.get(Topic, roadmap_item.topic_id)
            article_content = await llm_service.generate_article(
                topic_name=topic.name if topic else "Interview Prep",
                concept_name=roadmap_item.concept_title,
                user_skill_summary=str(user.skill_analysis) if user.skill_analysis else None
            )

            article = Article(
                roadmap_id=roadmap_item.id,
                title=roadmap_item.concept_title,
                slug=roadmap_item.concept_slug,
                eli5_content=article_content.get("eli5", ""),
                technical_content=article_content.get("technical", ""),
                code_snippets=article_content.get("code_snippets", []),
                real_world_examples=article_content.get("real_world", ""),
                practice_problems=article_content.get("practice", []),
            )
            db.add(article)

        # Update roadmap status
        roadmap_item.responded_at = datetime.utcnow()
        roadmap_item.status = "read"

        await db.commit()
        await db.refresh(article)

        # Send article link
        from app.core.config import settings
        article_url = f"{settings.FRONTEND_URL}/article/{article.id}"
        await whatsapp_service.send_article_link(
            to_number=user.phone_whatsapp,
            article_url=article_url,
            concept_title=roadmap_item.concept_title
        )

        logger.info(f"Processed response and sent article to user {user.id}")
        return True


# Singleton instance
scheduler_service = SchedulerService()
