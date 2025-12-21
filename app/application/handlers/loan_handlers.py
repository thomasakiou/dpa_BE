"""Loan handlers."""
from typing import List, Optional
from fastapi import HTTPException, status
from app.domain.repositories.loan_repository import ILoanRepository
from app.application.commands.loan_commands import (
    CreateLoanCommand, ApproveLoanCommand, DisburseLoanCommand,
    RecordLoanRepaymentCommand, CloseLoanCommand, RejectLoanCommand,
    UpdateLoanCommand, DeleteLoanCommand
)
from app.application.queries.queries import GetUserLoansQuery, GetAllLoansQuery
from app.domain.entities.loan import Loan, LoanStatus


class LoanHandler:
    """Handler for loan commands and queries."""
    
    def __init__(self, loan_repository: ILoanRepository):
        self.loan_repository = loan_repository
    
    # Commands
    def handle_create_loan(self, command: CreateLoanCommand) -> Loan:
        """Handle create loan command."""
        # Check if user already has an active loan
        active_loans = self.loan_repository.get_user_active_loans(command.user_id)
        if active_loans:
            # Policy: User can only have one active loan at a time (optional rule)
            # For now, we'll allow it but maybe warn or check business rules
            pass
            
        loan = Loan(
            user_id=command.user_id,
            loan_amount=command.loan_amount,
            interest_rate=command.interest_rate,
            duration_months=command.duration_months,
            description=command.description
        )
        
        # Calculate derived fields
        loan.monthly_repayment = loan._calculate_monthly_repayment()
        loan.total_repayable = loan._calculate_total_repayable()
        loan.balance = loan.total_repayable
        
        return self.loan_repository.create(loan)
    
    def handle_approve_loan(self, command: ApproveLoanCommand) -> Loan:
        """Handle approve loan command."""
        loan = self.loan_repository.get_by_id(command.loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
            
        if loan.status != LoanStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot approve loan in {loan.status} status"
            )
            
        loan.approve()
        return self.loan_repository.update(loan)
        
    def handle_disburse_loan(self, command: DisburseLoanCommand) -> Loan:
        """Handle disburse loan command."""
        loan = self.loan_repository.get_by_id(command.loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
            
        if loan.status != LoanStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot disburse loan in {loan.status} status"
            )
            
        loan.disburse()
        return self.loan_repository.update(loan)
        
    def handle_record_repayment(self, command: RecordLoanRepaymentCommand) -> Loan:
        """Handle record loan repayment command."""
        loan = self.loan_repository.get_by_id(command.loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
            
        if loan.status not in [LoanStatus.ACTIVE, LoanStatus.APPROVED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot record repayment for loan in {loan.status} status"
            )
            
        loan.record_repayment(command.amount)
        return self.loan_repository.update(loan)
        
    def handle_close_loan(self, command: CloseLoanCommand) -> Loan:
        """Handle close loan command."""
        loan = self.loan_repository.get_by_id(command.loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
            
        loan.close()
        return self.loan_repository.update(loan)
        
    def handle_reject_loan(self, command: RejectLoanCommand) -> Loan:
        """Handle reject loan command."""
        loan = self.loan_repository.get_by_id(command.loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
            
        if loan.status != LoanStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot reject loan in {loan.status} status"
            )
            
        loan.reject()
        return self.loan_repository.update(loan)
    
    def handle_update_loan(self, command: UpdateLoanCommand) -> Loan:
        """Handle update loan command."""
        loan = self.loan_repository.get_by_id(command.loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
            
        if command.loan_amount is not None:
            loan.loan_amount = command.loan_amount
        if command.interest_rate is not None:
            loan.interest_rate = command.interest_rate
        if command.duration_months is not None:
            loan.duration_months = command.duration_months
        if command.description is not None:
            loan.description = command.description
            
        # Recalculate derived fields if needed
        if any([command.loan_amount, command.interest_rate, command.duration_months]):
            loan.monthly_repayment = loan._calculate_monthly_repayment()
            loan.total_repayable = loan._calculate_total_repayable()
            # Only update balance if no payments made yet, otherwise complex logic needed
            if loan.amount_paid == 0:
                loan.balance = loan.total_repayable
            
        return self.loan_repository.update(loan)
        
    def handle_delete_loan(self, command: DeleteLoanCommand) -> bool:
        """Handle delete loan command."""
        return self.loan_repository.delete(command.loan_id)
    
    # Queries
    def handle_get_user_loans(self, query: GetUserLoansQuery) -> List[Loan]:
        """Handle get user loans query."""
        return self.loan_repository.get_by_user(
            query.user_id, skip=query.skip, limit=query.limit
        )
        
    def handle_get_all_loans(self, query: GetAllLoansQuery) -> List[Loan]:
        """Handle get all loans query."""
        return self.loan_repository.get_all(skip=query.skip, limit=query.limit)
