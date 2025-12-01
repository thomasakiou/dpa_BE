"""Shares API routes."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user_id
from app.infrastructure.repositories.share_repository_impl import ShareRepository
from app.application.handlers.share_handlers import ShareHandler
from app.application.queries.queries import GetUserSharesQuery
from app.presentation.schemas.share import ShareResponse

router = APIRouter()


@router.get("/me", response_model=List[ShareResponse])
def get_my_shares(
    skip: int = 0,
    limit: int = 100,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's shares."""
    share_repo = ShareRepository(db)
    handler = ShareHandler(share_repo)
    
    query = GetUserSharesQuery(
        user_id=user_id,
        skip=skip,
        limit=limit
    )
    
    return handler.handle_get_user_shares(query)


@router.get("/me/summary")
def get_my_shares_summary(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's shares summary."""
    share_repo = ShareRepository(db)
    total_count = share_repo.get_total_shares_by_user(user_id)
    total_value = share_repo.get_total_value_by_user(user_id)
    
    return {
        "total_shares": total_count,
        "total_value": total_value
    }
