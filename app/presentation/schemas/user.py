"""User schemas."""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.domain.entities.user import UserRole, UserStatus


class UserBase(BaseModel):
    """Base user schema."""
    member_id: str
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.MEMBER


class UserCreate(UserBase):
    """User creation schema."""
    password: str


class UserUpdate(BaseModel):
    """User update schema."""
    member_id: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""
    id: int
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
