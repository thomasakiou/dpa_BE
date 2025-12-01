"""Shares domain entity."""
from datetime import datetime
from typing import Optional
from decimal import Decimal


class Share:
    """Share domain entity representing member share contributions."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        shares_count: int = 0,
        share_value: Decimal = Decimal("0.00"),
        total_value: Decimal = Decimal("0.00"),
        purchase_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.shares_count = shares_count
        self.share_value = share_value
        self.total_value = total_value or (Decimal(shares_count) * share_value)
        self.purchase_date = purchase_date or datetime.utcnow()
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def add_shares(self, count: int, value_per_share: Decimal) -> None:
        """Add more shares to this entry."""
        self.shares_count += count
        self.share_value = value_per_share
        self.total_value = Decimal(self.shares_count) * self.share_value
        self.updated_at = datetime.utcnow()
    
    def update_share_value(self, new_value: Decimal) -> None:
        """Update the value per share and recalculate total."""
        self.share_value = new_value
        self.total_value = Decimal(self.shares_count) * self.share_value
        self.updated_at = datetime.utcnow()
    
    def calculate_total_value(self) -> Decimal:
        """Calculate total value of shares."""
        return Decimal(self.shares_count) * self.share_value
