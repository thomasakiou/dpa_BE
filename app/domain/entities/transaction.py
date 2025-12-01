"""Transaction domain entity."""
from enum import Enum
from datetime import datetime
from typing import Optional
from decimal import Decimal


class TransactionType(str, Enum):
    """Transaction type enumeration."""
    SAVINGS = "savings"
    SHARE = "share"
    LOAN_DISBURSEMENT = "loan_disbursement"
    LOAN_REPAYMENT = "loan_repayment"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"


class Transaction:
    """Transaction domain entity for financial ledger."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        transaction_type: TransactionType = TransactionType.DEPOSIT,
        description: str = "",
        debit: Decimal = Decimal("0.00"),
        credit: Decimal = Decimal("0.00"),
        balance: Decimal = Decimal("0.00"),
        reference_id: Optional[int] = None,
        transaction_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.transaction_type = transaction_type
        self.description = description
        self.debit = debit
        self.credit = credit
        self.balance = balance
        self.reference_id = reference_id
        self.transaction_date = transaction_date or datetime.utcnow()
        self.created_at = created_at or datetime.utcnow()
    
    def is_debit(self) -> bool:
        """Check if transaction is a debit."""
        return self.debit > Decimal("0.00")
    
    def is_credit(self) -> bool:
        """Check if transaction is a credit."""
        return self.credit > Decimal("0.00")
