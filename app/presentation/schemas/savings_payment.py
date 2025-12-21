"""Savings payment schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime
from enum import Enum


class SavingsPaymentTypeSchema(str, Enum):
    """Savings payment type enumeration for API."""
    MONTHLY_SAVINGS = "Monthly Savings"
    SHARE_PURCHASE = "Share Purchase"
    LOAN_REPAYMENT = "Loan Repayment"
    REGISTRATION_FEE = "Registration Fee"
    OTHER = "Other"


class SavingsPaymentCreate(BaseModel):
    """Schema for creating a savings payment."""
    user_id: int = Field(..., description="ID of the member")
    amount: Decimal = Field(..., description="Payment amount")
    type: SavingsPaymentTypeSchema = Field(..., description="Type of payment")
    payment_date: datetime = Field(..., description="Date of payment (ISO 8601)")
    payment_month: Optional[str] = Field(None, description="Month of payment (e.g., 'January', 'February')")
    description: Optional[str] = Field(None, description="Optional note")


class SavingsPaymentUpdate(BaseModel):
    """Schema for updating a savings payment."""
    user_id: Optional[int] = Field(None, description="ID of the member")
    amount: Optional[Decimal] = Field(None, description="Payment amount")
    type: Optional[SavingsPaymentTypeSchema] = Field(None, description="Type of payment")
    payment_date: Optional[datetime] = Field(None, description="Date of payment (ISO 8601)")
    payment_month: Optional[str] = Field(None, description="Month of payment (e.g., 'January', 'February')")
    description: Optional[str] = Field(None, description="Optional note")


class SavingsPaymentResponse(BaseModel):
    """Schema for savings payment response."""
    id: int
    user_id: int
    amount: Decimal
    type: SavingsPaymentTypeSchema
    payment_date: datetime
    payment_month: Optional[str]
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
