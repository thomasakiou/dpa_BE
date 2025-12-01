"""Authentication schemas."""
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Login request schema."""
    identifier: str
    password: str


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str
    user: dict


class ChangePasswordRequest(BaseModel):
    """Change password request schema."""
    old_password: str
    new_password: str
    confirm_password: str


class ResetPasswordRequest(BaseModel):
    """Reset password request schema (admin)."""
    new_password: str
