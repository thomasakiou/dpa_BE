"""Repository interface for User entity."""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.user import User


class IUserRepository(ABC):
    """Interface for User repository."""
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user."""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass
    
    @abstractmethod
    def get_by_member_id(self, member_id: str) -> Optional[User]:
        """Get user by member ID."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Update user."""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Count total users."""
        pass
