"""Savings payment domain entity."""
from enum import Enum
from datetime import datetime
from typing import Optional
from decimal import Decimal


class SavingsPaymentType(str, Enum):
    """Savings payment type enumeration."""
    MONTHLY_SAVINGS = "Monthly Savings"
    SHARE_PURCHASE = "Share Purchase"
    LOAN_REPAYMENT = "Loan Repayment"
    REGISTRATION_FEE = "Registration Fee"
    OTHER = "Other"


class SavingsPayment:
    """Savings payment domain entity representing individual payment records."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        amount: Decimal = Decimal("0.00"),
        type: SavingsPaymentType = SavingsPaymentType.MONTHLY_SAVINGS,
        payment_date: Optional[datetime] = None,
        payment_month: Optional[str] = None,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.type = type
        self.payment_date = payment_date or datetime.utcnow()
        self.payment_month = payment_month
        self.description = description
        self.created_at = created_at or datetime.utcnow()
        
        self._validate()
    
    def _validate(self) -> None:
        """Validate the savings payment."""
        if self.user_id <= 0:
            raise ValueError("User ID must be valid")
    
    def update(
        self,
        amount: Optional[Decimal] = None,
        type: Optional[SavingsPaymentType] = None,
        payment_date: Optional[datetime] = None,
        payment_month: Optional[str] = None,
        description: Optional[str] = None
    ) -> None:
        """Update payment details."""
        if amount is not None:
            self.amount = amount
        
        if type is not None:
            self.type = type
        
        if payment_date is not None:
            self.payment_date = payment_date
        
        if payment_month is not None:
            self.payment_month = payment_month
        
        if description is not None:
            self.description = description
