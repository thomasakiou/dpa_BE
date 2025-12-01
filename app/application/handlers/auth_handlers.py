"""Authentication handlers."""
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from app.domain.repositories.user_repository import IUserRepository
from app.application.commands.auth_commands import LoginCommand, ChangePasswordCommand, ResetPasswordCommand
from app.core.security import verify_password, get_password_hash, create_access_token
from app.domain.entities.user import User


class AuthHandler:
    """Handler for authentication commands."""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def handle_login(self, command: LoginCommand) -> Dict[str, Any]:
        """Handle login command."""
        # Try finding by email first
        user = self.user_repository.get_by_email(command.identifier)
        
        # If not found, try by member_id
        if not user:
            user = self.user_repository.get_by_member_id(command.identifier)
            
        if not user or not verify_password(command.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email/member ID or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        if not user.is_active():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
            
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role.value}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value
            }
        }
    
    def handle_change_password(self, command: ChangePasswordCommand) -> bool:
        """Handle change password command."""
        user = self.user_repository.get_by_id(command.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        if not verify_password(command.old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect old password"
            )
            
        user.hashed_password = get_password_hash(command.new_password)
        self.user_repository.update(user)
        return True
        
    def handle_reset_password(self, command: ResetPasswordCommand) -> bool:
        """Handle reset password command (admin)."""
        user = self.user_repository.get_by_id(command.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        user.hashed_password = get_password_hash(command.new_password)
        self.user_repository.update(user)
        return True
