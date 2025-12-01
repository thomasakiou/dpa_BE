"""Domain repositories package initialization."""
from app.domain.repositories.user_repository import IUserRepository
from app.domain.repositories.savings_repository import ISavingsRepository
from app.domain.repositories.share_repository import IShareRepository
from app.domain.repositories.loan_repository import ILoanRepository
from app.domain.repositories.transaction_repository import ITransactionRepository

__all__ = [
    "IUserRepository",
    "ISavingsRepository",
    "IShareRepository",
    "ILoanRepository",
    "ITransactionRepository",
]
