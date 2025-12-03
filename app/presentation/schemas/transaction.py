"""Transaction schemas."""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from app.domain.entities.transaction import TransactionType


class TransactionBase(BaseModel):
    """Base transaction schema."""
    amount: Decimal
    type: TransactionType
    payment_date: Optional[datetime] = None
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    """Transaction creation schema."""
    user_id: int


class TransactionUpdate(BaseModel):
    """Transaction update schema."""
    amount: Optional[Decimal] = None
    type: Optional[TransactionType] = None
    payment_date: Optional[datetime] = None
    description: Optional[str] = None


class TransactionResponse(TransactionBase):
    """Transaction response schema."""
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
