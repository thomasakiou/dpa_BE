"""User management commands."""
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.domain.entities.user import UserRole, UserStatus


class CreateUserCommand(BaseModel):
    """Command to create a new user."""
    member_id: str
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = ""
    role: UserRole = UserRole.MEMBER


class UpdateUserCommand(BaseModel):
    """Command to update user information."""
    user_id: int
    member_id: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None


class SuspendUserCommand(BaseModel):
    """Command to suspend a user."""
    user_id: int


class ActivateUserCommand(BaseModel):
    """Command to activate a user."""
    user_id: int


class DeleteUserCommand(BaseModel):
    """Command to delete a user."""
    user_id: int
