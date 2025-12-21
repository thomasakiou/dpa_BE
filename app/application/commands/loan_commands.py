"""Loan management commands."""
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import datetime


class CreateLoanCommand(BaseModel):
    """Command to create a loan application."""
    user_id: int
    loan_amount: Decimal
    interest_rate: Decimal
    duration_months: int
    description: Optional[str] = None


class ApproveLoanCommand(BaseModel):
    """Command to approve a loan."""
    loan_id: int


class DisburseLoanCommand(BaseModel):
    """Command to disburse a loan."""
    loan_id: int


class RecordLoanRepaymentCommand(BaseModel):
    """Command to record a loan repayment."""
    loan_id: int
    amount: Decimal


class CloseLoanCommand(BaseModel):
    """Command to close a loan."""
    loan_id: int


class RejectLoanCommand(BaseModel):
    """Command to reject a loan."""
    loan_id: int


class UpdateLoanCommand(BaseModel):
    """Command to update loan details."""
    loan_id: int
    loan_amount: Optional[Decimal] = None
    interest_rate: Optional[Decimal] = None
    duration_months: Optional[int] = None
    description: Optional[str] = None


class DeleteLoanCommand(BaseModel):
    """Command to delete a loan."""
    loan_id: int
