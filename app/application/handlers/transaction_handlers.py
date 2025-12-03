"""Transaction handlers."""
from typing import List, Optional
from fastapi import HTTPException, status
from app.domain.repositories.transaction_repository import ITransactionRepository
from app.application.commands.transaction_commands import (
    CreateTransactionCommand, UpdateTransactionCommand, DeleteTransactionCommand
)
from app.domain.entities.transaction import Transaction, TransactionType


class TransactionHandler:
    """Handler for transaction commands and queries."""
    
    def __init__(self, transaction_repository: ITransactionRepository):
        self.transaction_repository = transaction_repository
    
    def handle_create_transaction(self, command: CreateTransactionCommand) -> Transaction:
        """Handle create transaction command."""
        # Determine credit/debit based on type or amount sign?
        # Usually savings/repayment are credits (money coming in to the org/user account)
        # Withdrawals/disbursements are debits (money going out)
        
        # For simplicity, let's assume positive amount is credit, negative is debit?
        # Or use the type to decide.
        
        debit = 0
        credit = 0
        
        # Logic: 
        # Savings, Repayment, Share Purchase -> Credit (User paying money)
        # Withdrawal, Disbursement -> Debit (User receiving money)
        
        if command.transaction_type in [
            TransactionType.SAVINGS, 
            TransactionType.SHARE, 
            TransactionType.LOAN_REPAYMENT,
            TransactionType.DEPOSIT
        ]:
            credit = command.amount
        else:
            debit = command.amount
            
        transaction = Transaction(
            user_id=command.user_id,
            transaction_type=command.transaction_type,
            description=command.description or "",
            debit=debit,
            credit=credit,
            transaction_date=command.payment_date
        )
        
        return self.transaction_repository.create(transaction)
    
    def handle_update_transaction(self, command: UpdateTransactionCommand) -> Transaction:
        """Handle update transaction command."""
        transaction = self.transaction_repository.get_by_id(command.transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
            
        if command.transaction_type:
            transaction.transaction_type = command.transaction_type
            
        if command.description is not None:
            transaction.description = command.description
            
        if command.payment_date:
            transaction.transaction_date = command.payment_date
            
        if command.amount is not None:
            # Re-evaluate credit/debit
            t_type = command.transaction_type or transaction.transaction_type
            if t_type in [
                TransactionType.SAVINGS, 
                TransactionType.SHARE, 
                TransactionType.LOAN_REPAYMENT,
                TransactionType.DEPOSIT
            ]:
                transaction.credit = command.amount
                transaction.debit = 0
            else:
                transaction.debit = command.amount
                transaction.credit = 0
                
        # Note: Repository update method might need to be implemented/checked
        # The TransactionRepositoryImpl doesn't have an update method shown in previous view_file
        # I need to check if I need to add it.
        
        return transaction # Placeholder until repo update is verified
        
    def handle_delete_transaction(self, command: DeleteTransactionCommand) -> bool:
        """Handle delete transaction command."""
        # Repository delete method check needed
        return True # Placeholder
