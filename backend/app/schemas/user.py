from datetime import datetime, time
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class SkillAnalysis(BaseModel):
    """Schema for skill analysis results."""
    skills: List[str] = []
    experience_level: str = "beginner"  # beginner, intermediate, advanced
    strengths: List[str] = []
    weaknesses: List[str] = []
    recommended_topics: List[str] = []
    years_of_experience: Optional[int] = None
    tech_stack: List[str] = []


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: Optional[str] = None
    phone_whatsapp: Optional[str] = None
    timezone: str = "UTC"
    preferred_time: time = time(9, 0)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user response."""
    id: UUID
    email: str
    name: Optional[str] = None
    phone_whatsapp: Optional[str] = None
    resume_url: Optional[str] = None
    skill_analysis: Optional[Dict[str, Any]] = None
    experience_level: Optional[str] = None
    timezone: str
    preferred_time: time
    whatsapp_connected: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    name: Optional[str] = None
    phone_whatsapp: Optional[str] = None
    timezone: Optional[str] = None
    preferred_time: Optional[time] = None


class WhatsAppConnect(BaseModel):
    """Schema for WhatsApp connection."""
    phone_number: str = Field(..., pattern=r"^\+[1-9]\d{1,14}$")
