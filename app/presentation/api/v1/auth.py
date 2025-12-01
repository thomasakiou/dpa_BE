"""Authentication API routes."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user_id
from app.infrastructure.repositories.user_repository_impl import UserRepository
from app.application.handlers.auth_handlers import AuthHandler
from app.application.commands.auth_commands import LoginCommand, ChangePasswordCommand
from app.presentation.schemas.auth import LoginRequest, Token, ChangePasswordRequest

router = APIRouter()


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login user and return JWT token."""
    user_repo = UserRepository(db)
    handler = AuthHandler(user_repo)
    
    command = LoginCommand(
        identifier=request.identifier,
        password=request.password
    )
    
    return handler.handle_login(command)


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    request: ChangePasswordRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Change current user's password."""
    user_repo = UserRepository(db)
    handler = AuthHandler(user_repo)
    
    command = ChangePasswordCommand(
        user_id=user_id,
        old_password=request.old_password,
        new_password=request.new_password
    )
    
    handler.handle_change_password(command)
    return {"message": "Password changed successfully"}
