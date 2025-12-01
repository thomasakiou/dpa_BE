"""Share schemas."""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ShareBase(BaseModel):
    """Base share schema."""
    shares_count: int
    share_value: Decimal


class ShareCreate(ShareBase):
    """Share creation schema."""
    user_id: int
    purchase_date: Optional[datetime] = None


class ShareUpdate(BaseModel):
    """Share update schema."""
    shares_count: Optional[int] = None
    share_value: Optional[Decimal] = None


class ShareResponse(ShareBase):
    """Share response schema."""
    id: int
    user_id: int
    total_value: Decimal
    purchase_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
