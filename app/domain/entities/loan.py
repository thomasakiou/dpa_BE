"""Loan domain entity."""
from enum import Enum
from datetime import datetime
from typing import Optional
from decimal import Decimal


class LoanStatus(str, Enum):
    """Loan status enumeration."""
    PENDING = "pending"
    APPROVED = "approved"
    ACTIVE = "active"
    CLOSED = "closed"
    REJECTED = "rejected"


class Loan:
    """Loan domain entity representing member loans."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        loan_amount: Decimal = Decimal("0.00"),
        interest_rate: Decimal = Decimal("0.00"),
        duration_months: int = 0,
        monthly_repayment: Decimal = Decimal("0.00"),
        total_repayable: Decimal = Decimal("0.00"),
        amount_paid: Decimal = Decimal("0.00"),
        balance: Decimal = Decimal("0.00"),
        status: LoanStatus = LoanStatus.PENDING,
        application_date: Optional[datetime] = None,
        approval_date: Optional[datetime] = None,
        disbursement_date: Optional[datetime] = None,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.duration_months = duration_months
        self.monthly_repayment = monthly_repayment
        self.total_repayable = total_repayable or self._calculate_total_repayable()
        self.amount_paid = amount_paid
        self.balance = balance or self.total_repayable
        self.status = status
        self.application_date = application_date or datetime.utcnow()
        self.approval_date = approval_date
        self.disbursement_date = disbursement_date
        self.description = description
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def _calculate_total_repayable(self) -> Decimal:
        """Calculate total amount to be repaid including interest."""
        interest_amount = self.loan_amount * (self.interest_rate / Decimal("100"))
        return self.loan_amount + interest_amount
    
    def _calculate_monthly_repayment(self) -> Decimal:
        """Calculate monthly repayment amount."""
        if self.duration_months > 0:
            return self.total_repayable / Decimal(self.duration_months)
        return Decimal("0.00")
    
    def approve(self) -> None:
        """Approve the loan application."""
        self.status = LoanStatus.APPROVED
        self.approval_date = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def disburse(self) -> None:
        """Mark loan as disbursed and active."""
        self.status = LoanStatus.ACTIVE
        self.disbursement_date = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def record_repayment(self, amount: Decimal) -> None:
        """Record a loan repayment."""
        self.amount_paid += amount
        self.balance = self.total_repayable - self.amount_paid
        self.updated_at = datetime.utcnow()
        
        if self.balance <= Decimal("0.00"):
            self.balance = Decimal("0.00")
            self.close()
    
    def close(self) -> None:
        """Close the loan."""
        self.status = LoanStatus.CLOSED
        self.updated_at = datetime.utcnow()
    
    def reject(self) -> None:
        """Reject the loan application."""
        self.status = LoanStatus.REJECTED
        self.updated_at = datetime.utcnow()
    
    def is_fully_paid(self) -> bool:
        """Check if loan is fully paid."""
        return self.balance <= Decimal("0.00")
