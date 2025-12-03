"""Transaction management commands."""
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import datetime
from app.domain.entities.transaction import TransactionType


class CreateTransactionCommand(BaseModel):
    """Command to create a transaction."""
    user_id: int
    amount: Decimal
    transaction_type: TransactionType
    payment_date: Optional[datetime] = None
    description: Optional[str] = None


class UpdateTransactionCommand(BaseModel):
    """Command to update a transaction."""
    transaction_id: int
    amount: Optional[Decimal] = None
    transaction_type: Optional[TransactionType] = None
    payment_date: Optional[datetime] = None
    description: Optional[str] = None


class DeleteTransactionCommand(BaseModel):
    """Command to delete a transaction."""
    transaction_id: int
