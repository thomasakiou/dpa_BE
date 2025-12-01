"""Member API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user_id
from app.infrastructure.repositories.user_repository_impl import UserRepository
from app.application.handlers.user_handlers import UserHandler
from app.application.queries.queries import GetUserQuery
from app.presentation.schemas.user import UserResponse, UserUpdate
from app.application.commands.user_commands import UpdateUserCommand

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's profile."""
    user_repo = UserRepository(db)
    handler = UserHandler(user_repo)
    
    query = GetUserQuery(user_id=user_id)
    return handler.handle_get_user(query)


@router.put("/me", response_model=UserResponse)
def update_my_profile(
    request: UserUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update current user's profile."""
    user_repo = UserRepository(db)
    handler = UserHandler(user_repo)
    
    command = UpdateUserCommand(
        user_id=user_id,
        member_id=request.member_id,
        email=request.email,
        full_name=request.full_name,
        phone=request.phone
    )
    
    return handler.handle_update_user(command)


@router.get("/me/dashboard")
def get_my_dashboard(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's dashboard data."""
    # This would aggregate data from multiple repositories
    # For now returning placeholder structure
    return {
        "greeting": "Welcome back",
        "account_balance": 0.0,
        "total_savings": 0.0,
        "total_shares": 0.0,
        "loan_balance": 0.0,
        "recent_transactions": []
    }
