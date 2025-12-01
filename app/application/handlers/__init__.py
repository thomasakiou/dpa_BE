"""Application handlers package initialization."""
from app.application.handlers.auth_handlers import AuthHandler
from app.application.handlers.user_handlers import UserHandler
from app.application.handlers.savings_handlers import SavingsHandler
from app.application.handlers.share_handlers import ShareHandler
from app.application.handlers.loan_handlers import LoanHandler

__all__ = [
    "AuthHandler",
    "UserHandler",
    "SavingsHandler",
    "ShareHandler",
    "LoanHandler",
]
