"""Savings handlers."""
from typing import List, Optional
from fastapi import HTTPException, status
from app.domain.repositories.savings_repository import ISavingsRepository
from app.application.commands.savings_commands import (
    CreateSavingsCommand, RecordSavingsPaymentCommand, 
    UpdateSavingsCommand, DeleteSavingsCommand
)
from app.application.queries.queries import GetUserSavingsQuery, GetAllSavingsQuery
from app.domain.entities.savings import Savings, SavingsStatus


class SavingsHandler:
    """Handler for savings commands and queries."""
    
    def __init__(self, savings_repository: ISavingsRepository):
        self.savings_repository = savings_repository
    
    # Commands
    def handle_create_savings(self, command: CreateSavingsCommand) -> Savings:
        """Handle create savings command."""
        # Check if savings record already exists for this period
        existing = self.savings_repository.get_by_user_and_period(
            command.user_id, command.month, command.year
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Savings record already exists for {command.month} {command.year}"
            )
            
        savings = Savings(
            user_id=command.user_id,
            month=command.month,
            year=command.year,
            expected_amount=command.expected_amount,
            paid_amount=command.paid_amount
        )
        
        # Update status if paid amount > 0
        if command.paid_amount > 0:
            savings._update_status()
            
        return self.savings_repository.create(savings)
    
    def handle_record_payment(self, command: RecordSavingsPaymentCommand) -> Savings:
        """Handle record savings payment command."""
        savings = self.savings_repository.get_by_id(command.savings_id)
        if not savings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Savings record not found"
            )
            
        savings.record_payment(command.amount, command.payment_date)
        return self.savings_repository.update(savings)
    
    def handle_update_savings(self, command: UpdateSavingsCommand) -> Savings:
        """Handle update savings command."""
        savings = self.savings_repository.get_by_id(command.savings_id)
        if not savings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Savings record not found"
            )
            
        if command.expected_amount is not None:
            savings.expected_amount = command.expected_amount
        if command.paid_amount is not None:
            savings.paid_amount = command.paid_amount
            
        savings._update_status()
        return self.savings_repository.update(savings)
        
    def handle_delete_savings(self, command: DeleteSavingsCommand) -> bool:
        """Handle delete savings command."""
        return self.savings_repository.delete(command.savings_id)
    
    # Queries
    def handle_get_user_savings(self, query: GetUserSavingsQuery) -> List[Savings]:
        """Handle get user savings query."""
        return self.savings_repository.get_by_user(
            query.user_id, skip=query.skip, limit=query.limit
        )
        
    def handle_get_all_savings(self, query: GetAllSavingsQuery) -> List[Savings]:
        """Handle get all savings query."""
        return self.savings_repository.get_all(skip=query.skip, limit=query.limit)
