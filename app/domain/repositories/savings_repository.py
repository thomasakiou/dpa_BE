"""Repository interface for Savings entity."""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.savings import Savings
from decimal import Decimal


class ISavingsRepository(ABC):
    """Interface for Savings repository."""
    
    @abstractmethod
    def create(self, savings: Savings) -> Savings:
        """Create a new savings record."""
        pass
    
    @abstractmethod
    def get_by_id(self, savings_id: int) -> Optional[Savings]:
        """Get savings by ID."""
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Savings]:
        """Get all savings for a user."""
        pass
    
    @abstractmethod
    def get_by_user_and_period(self, user_id: int, month: str, year: int) -> Optional[Savings]:
        """Get savings for a specific month and year."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Savings]:
        """Get all savings with pagination."""
        pass
    
    @abstractmethod
    def update(self, savings: Savings) -> Savings:
        """Update savings record."""
        pass
    
    @abstractmethod
    def delete(self, savings_id: int) -> bool:
        """Delete savings record."""
        pass
    
    @abstractmethod
    def get_total_by_user(self, user_id: int) -> Decimal:
        """Get total savings amount for a user."""
        pass
    
    @abstractmethod
    def get_total_all_users(self) -> Decimal:
        """Get total savings amount for all users."""
        pass

    @abstractmethod
    def get_total_expected_by_user(self, user_id: int) -> Decimal:
        """Get total expected savings amount for a user."""
        pass
