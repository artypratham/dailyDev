from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.user_progress import UserProgress
from app.schemas.user import UserResponse, UserUpdate, SkillAnalysis
from app.services.resume_parser import resume_parser
from app.services.llm_service import llm_service

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile."""
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user's profile."""
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(current_user, field, value)

    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.post("/me/resume", response_model=SkillAnalysis)
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload and analyze resume."""
    # Validate file type
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are supported"
        )

    # Validate file size (max 5MB)
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 5MB"
        )

    # Parse resume
    resume_text = await resume_parser.parse(content, file.filename)
    if not resume_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not parse resume. Please try a different file."
        )

    # Analyze with LLM
    skill_analysis = await llm_service.analyze_resume(resume_text)

    # Update user
    current_user.skill_analysis = skill_analysis
    current_user.experience_level = skill_analysis.get("experience_level", "beginner")
    # In production, upload file to S3/R2 and store URL
    # current_user.resume_url = uploaded_url

    await db.commit()
    await db.refresh(current_user)

    return SkillAnalysis(**skill_analysis)


@router.get("/me/stats")
async def get_user_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's learning statistics."""
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == current_user.id)
    )
    progress_records = result.scalars().all()

    total_streak = max([p.streak_count for p in progress_records], default=0)
    total_concepts = sum([p.total_concepts_learned for p in progress_records])
    total_articles = sum([p.total_articles_read for p in progress_records])
    all_badges = []
    for p in progress_records:
        if p.badges:
            all_badges.extend(p.badges)

    return {
        "current_streak": total_streak,
        "longest_streak": max([p.longest_streak for p in progress_records], default=0),
        "total_concepts_learned": total_concepts,
        "total_articles_read": total_articles,
        "badges": list(set(all_badges)),
        "topics_in_progress": len([p for p in progress_records if p.total_concepts_learned > 0]),
    }


@router.post("/me/whatsapp/connect")
async def connect_whatsapp(
    phone_number: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Connect WhatsApp number to user account."""
    # Basic phone number validation
    if not phone_number.startswith("+"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number must include country code (e.g., +1234567890)"
        )

    # Check if phone already used by another user
    result = await db.execute(
        select(User).where(
            User.phone_whatsapp == phone_number,
            User.id != current_user.id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered to another account"
        )

    current_user.phone_whatsapp = phone_number
    current_user.whatsapp_connected = "connected"

    await db.commit()

    return {
        "message": "WhatsApp connected successfully",
        "phone": phone_number,
        "instructions": (
            "For Twilio Sandbox: Send 'join <your-sandbox-code>' to +1 415 523 8886 on WhatsApp "
            "to complete the connection."
        )
    }
