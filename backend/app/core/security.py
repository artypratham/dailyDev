"""
Security utilities for authentication and authorization.
Uses bcrypt for password hashing and JWT for tokens.
"""
from datetime import datetime, timedelta
from typing import Optional, Any
import uuid
import bcrypt
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.core.logging_config import get_user_journey_logger, JourneyType

# JWT Bearer
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash using bcrypt."""
    log = get_user_journey_logger(JourneyType.LOGIN)
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        result = bcrypt.checkpw(password_bytes, hashed_bytes)
        log.debug(f"Password verification completed")
        return result
    except Exception as e:
        log.error(f"Password verification failed: {str(e)}")
        return False


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    log = get_user_journey_logger(JourneyType.SIGNUP)
    try:
        # Truncate password to 72 bytes (bcrypt limit)
        password_bytes = password.encode('utf-8')[:72]
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        log.debug("Password hashed successfully")
        return hashed.decode('utf-8')
    except Exception as e:
        log.error(f"Password hashing failed: {str(e)}")
        raise


def create_access_token(
    subject: str | Any,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    log = get_user_journey_logger(JourneyType.LOGIN, user_id=str(subject))
    try:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        log.info(f"Access token created, expires at {expire}")
        return encoded_jwt
    except Exception as e:
        log.error(f"Token creation failed: {str(e)}")
        raise


def decode_access_token(token: str) -> Optional[str]:
    """Decode a JWT access token and return the subject."""
    log = get_user_journey_logger(JourneyType.LOGIN)
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        log.debug(f"Token decoded successfully")
        return user_id
    except JWTError as e:
        log.warning(f"Token decode failed: {str(e)}")
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get the current authenticated user from JWT token."""
    from app.models.user import User  # Import here to avoid circular imports

    request_id = str(uuid.uuid4())[:8]
    log = get_user_journey_logger(JourneyType.LOGIN, request_id=request_id)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    log.debug("Validating user token")

    user_id = decode_access_token(token)

    if user_id is None:
        log.warning("Token validation failed - invalid token")
        raise credentials_exception

    log = get_user_journey_logger(JourneyType.LOGIN, user_id=user_id, request_id=request_id)
    log.debug(f"Looking up user in database")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        log.warning(f"User not found in database")
        raise credentials_exception

    log.info(f"User authenticated successfully")
    return user
