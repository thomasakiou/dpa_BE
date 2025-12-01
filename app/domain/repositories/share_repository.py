"""Repository interface for Share entity."""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.share import Share
from decimal import Decimal


class IShareRepository(ABC):
    """Interface for Share repository."""
    
    @abstractmethod
    def create(self, share: Share) -> Share:
        """Create a new share record."""
        pass
    
    @abstractmethod
    def get_by_id(self, share_id: int) -> Optional[Share]:
        """Get share by ID."""
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Share]:
        """Get all shares for a user."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Share]:
        """Get all shares with pagination."""
        pass
    
    @abstractmethod
    def update(self, share: Share) -> Share:
        """Update share record."""
        pass
    
    @abstractmethod
    def delete(self, share_id: int) -> bool:
        """Delete share record."""
        pass
    
    @abstractmethod
    def get_total_shares_by_user(self, user_id: int) -> int:
        """Get total number of shares for a user."""
        pass
    
    @abstractmethod
    def get_total_value_by_user(self, user_id: int) -> Decimal:
        """Get total value of shares for a user."""
        pass
    
    @abstractmethod
    def get_total_value_all_users(self) -> Decimal:
        """Get total value of shares for all users."""
        pass
