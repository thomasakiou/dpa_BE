"""Savings payment handlers."""
from typing import List
from fastapi import HTTPException, status
from app.domain.repositories.savings_payment_repository import ISavingsPaymentRepository
from app.application.commands.savings_payment_commands import (
    CreateSavingsPaymentCommand,
    UpdateSavingsPaymentCommand,
    DeleteSavingsPaymentCommand
)
from app.application.queries.queries import GetAllSavingsPaymentsQuery, GetSavingsPaymentByIdQuery
from app.domain.entities.savings_payment import SavingsPayment


class SavingsPaymentHandler:
    """Handler for savings payment commands and queries."""
    
    def __init__(self, repository: ISavingsPaymentRepository):
        self.repository = repository
    
    def handle_create_payment(self, command: CreateSavingsPaymentCommand) -> SavingsPayment:
        """Handle create savings payment command."""
        payment = SavingsPayment(
            user_id=command.user_id,
            amount=command.amount,
            type=command.type,
            payment_date=command.payment_date,
            payment_month=command.payment_month,
            description=command.description
        )
        
        return self.repository.create(payment)
    
    def handle_update_payment(self, command: UpdateSavingsPaymentCommand) -> SavingsPayment:
        """Handle update savings payment command."""
        payment = self.repository.get_by_id(command.payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Savings payment with id {command.payment_id} not found"
            )
        
        payment.update(
            amount=command.amount,
            type=command.type,
            payment_date=command.payment_date,
            payment_month=command.payment_month,
            description=command.description
        )
        
        return self.repository.update(payment)
    
    def handle_delete_payment(self, command: DeleteSavingsPaymentCommand) -> bool:
        """Handle delete savings payment command."""
        success = self.repository.delete(command.payment_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Savings payment with id {command.payment_id} not found"
            )
        return success
    
    def handle_get_all_payments(self, query: GetAllSavingsPaymentsQuery) -> List[SavingsPayment]:
        """Handle get all savings payments query."""
        return self.repository.get_all(skip=query.skip, limit=query.limit)
    
    def handle_get_payment_by_id(self, query: GetSavingsPaymentByIdQuery) -> SavingsPayment:
        """Handle get savings payment by ID query."""
        payment = self.repository.get_by_id(query.payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Savings payment with id {query.payment_id} not found"
            )
        return payment

    def handle_get_user_payments(self, user_id: int, skip: int = 0, limit: int = 100) -> List[SavingsPayment]:
        """Handle get savings payments for a specific user."""
        return self.repository.get_by_user(user_id, skip, limit)

    def handle_get_total_paid_by_user(self, user_id: int) -> float:
        """Handle get total amount paid by a user."""
        return self.repository.get_total_paid_by_user(user_id)

    def handle_get_count_by_user(self, user_id: int) -> int:
        """Handle get total count of payments for a user."""
        return self.repository.get_count_by_user(user_id)
