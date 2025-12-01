"""Savings domain entity."""
from enum import Enum
from datetime import datetime
from typing import Optional
from decimal import Decimal


class SavingsStatus(str, Enum):
    """Savings payment status enumeration."""
    PAID = "paid"
    PENDING = "pending"
    PARTIAL = "partial"
    MISSED = "missed"


class Savings:
    """Savings domain entity representing monthly member savings."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        month: str = "",
        year: int = 0,
        expected_amount: Decimal = Decimal("0.00"),
        paid_amount: Decimal = Decimal("0.00"),
        status: SavingsStatus = SavingsStatus.PENDING,
        payment_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.month = month
        self.year = year
        self.expected_amount = expected_amount
        self.paid_amount = paid_amount
        self.status = status
        self.payment_date = payment_date
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def record_payment(self, amount: Decimal, payment_date: Optional[datetime] = None) -> None:
        """Record a payment for this savings entry."""
        self.paid_amount += amount
        self.payment_date = payment_date or datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self._update_status()
    
    def _update_status(self) -> None:
        """Update status based on paid amount."""
        if self.paid_amount >= self.expected_amount:
            self.status = SavingsStatus.PAID
        elif self.paid_amount > Decimal("0.00"):
            self.status = SavingsStatus.PARTIAL
        else:
            self.status = SavingsStatus.PENDING
    
    def is_fully_paid(self) -> bool:
        """Check if savings is fully paid."""
        return self.paid_amount >= self.expected_amount
    
    def remaining_amount(self) -> Decimal:
        """Calculate remaining amount to be paid."""
        return max(self.expected_amount - self.paid_amount, Decimal("0.00"))
