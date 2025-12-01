"""Savings management commands."""
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import datetime


class CreateSavingsCommand(BaseModel):
    """Command to create a savings record."""
    user_id: int
    month: str
    year: int
    expected_amount: Decimal
    paid_amount: Decimal = Decimal("0.00")


class RecordSavingsPaymentCommand(BaseModel):
    """Command to record a savings payment."""
    savings_id: int
    amount: Decimal
    payment_date: Optional[datetime] = None


class UpdateSavingsCommand(BaseModel):
    """Command to update savings record."""
    savings_id: int
    expected_amount: Optional[Decimal] = None
    paid_amount: Optional[Decimal] = None


class DeleteSavingsCommand(BaseModel):
    """Command to delete a savings record."""
    savings_id: int
