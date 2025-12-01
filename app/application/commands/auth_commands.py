"""Authentication commands."""
from pydantic import BaseModel, EmailStr


class LoginCommand(BaseModel):
    """Command to login a user."""
    identifier: str  # Can be email or member_id
    password: str


class ChangePasswordCommand(BaseModel):
    """Command to change user password."""
    user_id: int
    old_password: str
    new_password: str


class ResetPasswordCommand(BaseModel):
    """Command to reset user password (admin only)."""
    user_id: int
    new_password: str
