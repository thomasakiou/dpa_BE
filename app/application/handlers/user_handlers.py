"""User handlers."""
from typing import List, Optional
from fastapi import HTTPException, status
from app.domain.repositories.user_repository import IUserRepository
from app.application.commands.user_commands import (
    CreateUserCommand, UpdateUserCommand, SuspendUserCommand, 
    ActivateUserCommand, DeleteUserCommand, ResetPasswordCommand
)
from app.application.queries.queries import GetUserQuery, GetUsersQuery
from app.domain.entities.user import User, UserRole, UserStatus
from app.core.security import get_password_hash


class UserHandler:
    """Handler for user commands and queries."""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    # Commands
    def handle_create_user(self, command: CreateUserCommand) -> User:
        """Handle create user command."""
        if self.user_repository.get_by_email(command.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        if self.user_repository.get_by_member_id(command.member_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member ID already registered"
            )
            
        user = User(
            member_id=command.member_id,
            email=command.email,
            hashed_password=get_password_hash(command.password),
            full_name=command.full_name,
            phone=command.phone,
            role=command.role,
            status=UserStatus.ACTIVE
        )
        
        return self.user_repository.create(user)
    
    def handle_update_user(self, command: UpdateUserCommand) -> User:
        """Handle update user command."""
        user = self.user_repository.get_by_id(command.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        if command.email and command.email != user.email:
            if self.user_repository.get_by_email(command.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            user.email = command.email
            
        if command.member_id and command.member_id != user.member_id:
            if self.user_repository.get_by_member_id(command.member_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Member ID already registered"
                )
            user.member_id = command.member_id
            
        if command.full_name:
            user.full_name = command.full_name
        if command.phone is not None:
            user.phone = command.phone
            
        return self.user_repository.update(user)
    
    def handle_suspend_user(self, command: SuspendUserCommand) -> User:
        """Handle suspend user command."""
        user = self.user_repository.get_by_id(command.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        user.suspend()
        return self.user_repository.update(user)
    
    def handle_activate_user(self, command: ActivateUserCommand) -> User:
        """Handle activate user command."""
        user = self.user_repository.get_by_id(command.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        user.activate()
        return self.user_repository.update(user)
        
    def handle_delete_user(self, command: DeleteUserCommand) -> bool:
        """Handle delete user command."""
        return self.user_repository.delete(command.user_id)
    
    def handle_reset_password(self, command: ResetPasswordCommand) -> User:
        """Handle reset password command."""
        user = self.user_repository.get_by_id(command.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Hash the new password and update the user
        user.hashed_password = get_password_hash(command.new_password)
        return self.user_repository.update(user)

    
    # Queries
    def handle_get_user(self, query: GetUserQuery) -> User:
        """Handle get user query."""
        user = self.user_repository.get_by_id(query.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
        
    def handle_get_users(self, query: GetUsersQuery) -> List[User]:
        """Handle get users query."""
        return self.user_repository.get_all(skip=query.skip, limit=query.limit)
