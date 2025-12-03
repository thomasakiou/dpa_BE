"""Savings API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user_id
from app.infrastructure.repositories.savings_repository_impl import SavingsRepository
from app.infrastructure.repositories.savings_payment_repository_impl import SavingsPaymentRepository
from app.application.handlers.savings_handlers import SavingsHandler
from app.application.handlers.savings_payment_handlers import SavingsPaymentHandler
from app.application.queries.queries import GetUserSavingsQuery
from app.presentation.schemas.savings import SavingsResponse
from app.presentation.schemas.savings_payment import SavingsPaymentResponse


router = APIRouter()


@router.get("/me", response_model=List[SavingsPaymentResponse])
def get_my_savings(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's savings history (payments). Returns all records without pagination."""
    payment_repo = SavingsPaymentRepository(db)
    handler = SavingsPaymentHandler(payment_repo)
    
    return handler.handle_get_user_payments(user_id=user_id, skip=0, limit=None)


@router.get("/me/summary")
def get_my_savings_summary(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's savings summary."""
    savings_repo = SavingsRepository(db)
    payment_repo = SavingsPaymentRepository(db)
    
    payment_handler = SavingsPaymentHandler(payment_repo)
    
    total_paid = payment_handler.handle_get_total_paid_by_user(user_id)
    payment_count = payment_handler.handle_get_count_by_user(user_id)
    total_expected = savings_repo.get_total_expected_by_user(user_id)
    
    return {
        "total_paid": total_paid,
        "total_expected": total_expected,
        "payment_count": payment_count
    }
