"""Loan schemas."""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from app.domain.entities.loan import LoanStatus


class LoanBase(BaseModel):
    """Base loan schema."""
    loan_amount: Decimal
    interest_rate: Decimal
    duration_months: int
    description: Optional[str] = None


class LoanCreate(LoanBase):
    """Loan creation schema."""
    user_id: int


class LoanUpdate(BaseModel):
    """Loan update schema."""
    loan_amount: Optional[Decimal] = None
    interest_rate: Optional[Decimal] = None
    duration_months: Optional[int] = None
    description: Optional[str] = None


class LoanRepayment(BaseModel):
    """Loan repayment schema."""
    amount: Decimal


class LoanResponse(LoanBase):
    """Loan response schema."""
    id: int
    user_id: int
    monthly_repayment: Decimal
    total_repayable: Decimal
    amount_paid: Decimal
    balance: Decimal
    status: LoanStatus
    application_date: datetime
    approval_date: Optional[datetime]
    disbursement_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
