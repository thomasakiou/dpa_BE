"""Admin API routes."""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, require_admin
from app.infrastructure.repositories.user_repository_impl import UserRepository
from app.application.handlers.user_handlers import UserHandler
from app.application.queries.queries import GetUsersQuery
from app.application.commands.user_commands import CreateUserCommand, SuspendUserCommand, ActivateUserCommand
from app.presentation.schemas.user import UserResponse, UserCreate

router = APIRouter()


@router.get("/dashboard", dependencies=[Depends(require_admin)])
def get_admin_dashboard(db: Session = Depends(get_db)):
    """Get admin dashboard analytics."""
    # Placeholder for admin dashboard data aggregation
    return {
        "total_members": 0,
        "total_savings": 0.0,
        "total_shares": 0.0,
        "total_loans": 0.0,
        "outstanding_balances": 0.0
    }


@router.get("/users", response_model=List[UserResponse], dependencies=[Depends(require_admin)])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all users (admin only)."""
    user_repo = UserRepository(db)
    handler = UserHandler(user_repo)
    
    query = GetUsersQuery(skip=skip, limit=limit)
    return handler.handle_get_users(query)


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_user(
    request: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user (admin only)."""
    user_repo = UserRepository(db)
    handler = UserHandler(user_repo)
    
    command = CreateUserCommand(
        member_id=request.member_id,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        phone=request.phone,
        role=request.role
    )
    
    return handler.handle_create_user(command)


@router.post("/users/{user_id}/suspend", response_model=UserResponse, dependencies=[Depends(require_admin)])
def suspend_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Suspend a user (admin only)."""
    user_repo = UserRepository(db)
    handler = UserHandler(user_repo)
    
    command = SuspendUserCommand(user_id=user_id)
    return handler.handle_suspend_user(command)


@router.post("/users/{user_id}/activate", response_model=UserResponse, dependencies=[Depends(require_admin)])
def activate_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Activate a user (admin only)."""
    user_repo = UserRepository(db)
    handler = UserHandler(user_repo)
    
    command = ActivateUserCommand(user_id=user_id)
    return handler.handle_activate_user(command)
