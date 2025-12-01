"""Repository interface for Loan entity."""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.loan import Loan, LoanStatus
from decimal import Decimal


class ILoanRepository(ABC):
    """Interface for Loan repository."""
    
    @abstractmethod
    def create(self, loan: Loan) -> Loan:
        """Create a new loan."""
        pass
    
    @abstractmethod
    def get_by_id(self, loan_id: int) -> Optional[Loan]:
        """Get loan by ID."""
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Loan]:
        """Get all loans for a user."""
        pass
    
    @abstractmethod
    def get_by_status(self, status: LoanStatus, skip: int = 0, limit: int = 100) -> List[Loan]:
        """Get loans by status."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Loan]:
        """Get all loans with pagination."""
        pass
    
    @abstractmethod
    def update(self, loan: Loan) -> Loan:
        """Update loan."""
        pass
    
    @abstractmethod
    def delete(self, loan_id: int) -> bool:
        """Delete loan."""
        pass
    
    @abstractmethod
    def get_total_disbursed(self) -> Decimal:
        """Get total amount of disbursed loans."""
        pass
    
    @abstractmethod
    def get_total_outstanding(self) -> Decimal:
        """Get total outstanding loan balance."""
        pass
    
    @abstractmethod
    def get_user_active_loans(self, user_id: int) -> List[Loan]:
        """Get active loans for a user."""
        pass
