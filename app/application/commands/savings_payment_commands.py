"""Savings payment commands."""
from decimal import Decimal
from datetime import datetime
from typing import Optional
from app.domain.entities.savings_payment import SavingsPaymentType


class CreateSavingsPaymentCommand:
    """Command to create a new savings payment."""
    
    def __init__(
        self,
        user_id: int,
        amount: Decimal,
        type: SavingsPaymentType,
        payment_date: datetime,
        payment_month: Optional[str] = None,
        description: Optional[str] = None
    ):
        self.user_id = user_id
        self.amount = amount
        self.type = type
        self.payment_date = payment_date
        self.payment_month = payment_month
        self.description = description


class UpdateSavingsPaymentCommand:
    """Command to update an existing savings payment."""
    
    def __init__(
        self,
        payment_id: int,
        amount: Optional[Decimal] = None,
        type: Optional[SavingsPaymentType] = None,
        payment_date: Optional[datetime] = None,
        payment_month: Optional[str] = None,
        description: Optional[str] = None
    ):
        self.payment_id = payment_id
        self.amount = amount
        self.type = type
        self.payment_date = payment_date
        self.payment_month = payment_month
        self.description = description


class DeleteSavingsPaymentCommand:
    """Command to delete a savings payment."""
    
    def __init__(self, payment_id: int):
        self.payment_id = payment_id
