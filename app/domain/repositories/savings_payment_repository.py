"""Savings payment repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal
from app.domain.entities.savings_payment import SavingsPayment


class ISavingsPaymentRepository(ABC):
    """Interface for savings payment repository."""
    
    @abstractmethod
    def create(self, payment: SavingsPayment) -> SavingsPayment:
        """Create a new savings payment record."""
        pass
    
    @abstractmethod
    def get_by_id(self, payment_id: int) -> Optional[SavingsPayment]:
        """Get a savings payment by ID."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SavingsPayment]:
        """Get all savings payment records with pagination."""
        pass
    
    @abstractmethod
    def update(self, payment: SavingsPayment) -> SavingsPayment:
        """Update an existing savings payment record."""
        pass
    
    @abstractmethod
    def delete(self, payment_id: int) -> bool:
        """Delete a savings payment record."""
        pass

    @abstractmethod
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[SavingsPayment]:
        """Get all savings payments for a specific user."""
        pass

    @abstractmethod
    def get_total_paid_by_user(self, user_id: int) -> Decimal:
        """Get total amount paid by a user."""
        pass

    @abstractmethod
    def get_count_by_user(self, user_id: int) -> int:
        """Get total count of payments for a user."""
        pass
