"""Savings schemas."""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from app.domain.entities.savings import SavingsStatus


class SavingsBase(BaseModel):
    """Base savings schema."""
    month: str
    year: int
    expected_amount: Decimal


class SavingsCreate(SavingsBase):
    """Savings creation schema."""
    user_id: int
    paid_amount: Decimal = Decimal("0.00")


class SavingsPayment(BaseModel):
    """Savings payment schema."""
    amount: Decimal
    payment_date: Optional[datetime] = None


class SavingsUpdate(BaseModel):
    """Savings update schema."""
    expected_amount: Optional[Decimal] = None
    paid_amount: Optional[Decimal] = None


class SavingsResponse(SavingsBase):
    """Savings response schema."""
    id: int
    user_id: int
    paid_amount: Decimal
    status: SavingsStatus
    payment_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
