"""Domain entities for the DPA application."""
from enum import Enum
from datetime import datetime
from typing import Optional


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    MEMBER = "member"


class UserStatus(str, Enum):
    """User status enumeration."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


class User:
    """User domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        member_id: str = "",
        email: str = "",
        hashed_password: str = "",
        full_name: str = "",
        phone: str = "",
        role: UserRole = UserRole.MEMBER,
        status: UserStatus = UserStatus.ACTIVE,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_id = member_id
        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.phone = phone
        self.role = role
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def is_admin(self) -> bool:
        """Check if user is an admin."""
        return self.role == UserRole.ADMIN
    
    def is_active(self) -> bool:
        """Check if user is active."""
        return self.status == UserStatus.ACTIVE
    
    def suspend(self) -> None:
        """Suspend the user."""
        self.status = UserStatus.SUSPENDED
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate the user."""
        self.status = UserStatus.ACTIVE
        self.updated_at = datetime.utcnow()
