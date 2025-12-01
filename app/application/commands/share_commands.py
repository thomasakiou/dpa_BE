"""Share management commands."""
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import datetime


class CreateShareCommand(BaseModel):
    """Command to create a share record."""
    user_id: int
    shares_count: int
    share_value: Decimal
    purchase_date: Optional[datetime] = None


class UpdateShareCommand(BaseModel):
    """Command to update share record."""
    share_id: int
    shares_count: Optional[int] = None
    share_value: Optional[Decimal] = None


class DeleteShareCommand(BaseModel):
    """Command to delete a share record."""
    share_id: int
