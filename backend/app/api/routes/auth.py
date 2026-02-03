"""
Authentication routes for signup, login, and user info.
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.logging_config import get_user_journey_logger, JourneyType

router = APIRouter()


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    request_id = str(uuid.uuid4())[:8]
    log = get_user_journey_logger(JourneyType.SIGNUP, request_id=request_id)

    log.info(f"=== SIGNUP STARTED === email={user_data.email}")
    log.debug(f"Signup request received - name={user_data.name}, has_phone={bool(user_data.phone_whatsapp)}")

    try:
        # Step 1: Check if email already exists
        log.debug(f"Step 1: Checking if email already exists")
        result = await db.execute(select(User).where(User.email == user_data.email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            log.warning(f"Signup failed - email already registered: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        log.debug(f"Email check passed - email is available")

        # Step 2: Check if phone already exists (if provided)
        if user_data.phone_whatsapp:
            log.debug(f"Step 2: Checking if phone already exists")
            result = await db.execute(
                select(User).where(User.phone_whatsapp == user_data.phone_whatsapp)
            )
            if result.scalar_one_or_none():
                log.warning(f"Signup failed - phone already registered")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already registered"
                )
            log.debug(f"Phone check passed - phone is available")
        else:
            log.debug(f"Step 2: Skipped - no phone provided")

        # Step 3: Hash password
        log.debug(f"Step 3: Hashing password")
        password_hash = get_password_hash(user_data.password)
        log.debug(f"Password hashed successfully")

        # Step 4: Create user object
        log.debug(f"Step 4: Creating user object")
        user = User(
            email=user_data.email,
            password_hash=password_hash,
            name=user_data.name,
            phone_whatsapp=user_data.phone_whatsapp,
            timezone=user_data.timezone,
            preferred_time=user_data.preferred_time,
        )

        # Step 5: Save to database
        log.debug(f"Step 5: Saving user to database")
        db.add(user)
        await db.commit()
        await db.refresh(user)
        log.info(f"User created successfully - user_id={user.id}")

        # Step 6: Generate token
        log.debug(f"Step 6: Generating access token")
        access_token = create_access_token(subject=str(user.id))
        log.info(f"=== SIGNUP COMPLETED SUCCESSFULLY === user_id={user.id}")

        return Token(access_token=access_token)

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        log.error(f"=== SIGNUP FAILED === error={str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Signup failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return token."""
    request_id = str(uuid.uuid4())[:8]
    log = get_user_journey_logger(JourneyType.LOGIN, request_id=request_id)

    log.info(f"=== LOGIN STARTED === email={user_data.email}")

    try:
        # Step 1: Find user by email
        log.debug(f"Step 1: Looking up user by email")
        result = await db.execute(select(User).where(User.email == user_data.email))
        user = result.scalar_one_or_none()

        if not user:
            log.warning(f"Login failed - user not found: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        log.debug(f"User found - user_id={user.id}")

        # Step 2: Verify password
        log.debug(f"Step 2: Verifying password")
        if not verify_password(user_data.password, user.password_hash):
            log.warning(f"Login failed - incorrect password for user_id={user.id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        log.debug(f"Password verified successfully")

        # Step 3: Generate token
        log.debug(f"Step 3: Generating access token")
        access_token = create_access_token(subject=str(user.id))
        log.info(f"=== LOGIN COMPLETED SUCCESSFULLY === user_id={user.id}")

        return Token(access_token=access_token)

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"=== LOGIN FAILED === error={str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user information."""
    log = get_user_journey_logger(JourneyType.LOGIN, user_id=str(current_user.id))
    log.info(f"User info requested - user_id={current_user.id}")
    return current_user
