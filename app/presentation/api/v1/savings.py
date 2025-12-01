"""Savings API routes."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user_id
from app.infrastructure.repositories.savings_repository_impl import SavingsRepository
from app.application.handlers.savings_handlers import SavingsHandler
from app.application.queries.queries import GetUserSavingsQuery
from app.presentation.schemas.savings import SavingsResponse

router = APIRouter()


@router.get("/me", response_model=List[SavingsResponse])
def get_my_savings(
    skip: int = 0,
    limit: int = 100,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's savings history."""
    savings_repo = SavingsRepository(db)
    handler = SavingsHandler(savings_repo)
    
    query = GetUserSavingsQuery(
        user_id=user_id,
        skip=skip,
        limit=limit
    )
    
    return handler.handle_get_user_savings(query)


@router.get("/me/summary")
def get_my_savings_summary(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's savings summary."""
    savings_repo = SavingsRepository(db)
    total = savings_repo.get_total_by_user(user_id)
    
    return {
        "total_contribution": total,
        "missing_months": 0  # To be implemented with logic
    }
