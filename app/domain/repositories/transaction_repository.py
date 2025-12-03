"""Repository interface for Transaction entity."""
from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from app.domain.entities.transaction import Transaction, TransactionType


class ITransactionRepository(ABC):
    """Interface for Transaction repository."""
    
    @abstractmethod
    def create(self, transaction: Transaction) -> Transaction:
        """Create a new transaction."""
        pass
    
    @abstractmethod
    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID."""
        pass
    
    @abstractmethod
    def get_by_user(
        self, 
        user_id: int, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Transaction]:
        """Get transactions for a user with optional date filtering."""
        pass
    
    @abstractmethod
    def get_by_type(
        self, 
        transaction_type: TransactionType,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Transaction]:
        """Get transactions by type."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Transaction]:
        """Get all transactions with pagination."""
        pass

    @abstractmethod
    def update(self, transaction: Transaction) -> Transaction:
        """Update transaction."""
        pass

    @abstractmethod
    def delete(self, transaction_id: int) -> bool:
        """Delete transaction."""
        pass
