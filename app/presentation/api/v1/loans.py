"""Loans API routes."""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user_id
from app.infrastructure.repositories.loan_repository_impl import LoanRepository
from app.application.handlers.loan_handlers import LoanHandler
from app.application.queries.queries import GetUserLoansQuery
from app.application.commands.loan_commands import CreateLoanCommand
from app.presentation.schemas.loan import LoanResponse, LoanCreate

router = APIRouter()


@router.get("/me", response_model=List[LoanResponse])
def get_my_loans(
    skip: int = 0,
    limit: int = 100,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's loans."""
    loan_repo = LoanRepository(db)
    handler = LoanHandler(loan_repo)
    
    query = GetUserLoansQuery(
        user_id=user_id,
        skip=skip,
        limit=limit
    )
    
    return handler.handle_get_user_loans(query)


@router.post("/apply", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def apply_for_loan(
    request: LoanCreate,
    db: Session = Depends(get_db)
):
    """Apply for a new loan."""
    loan_repo = LoanRepository(db)
    handler = LoanHandler(loan_repo)
    
    command = CreateLoanCommand(
        user_id=request.user_id,
        loan_amount=request.loan_amount,
        interest_rate=request.interest_rate,
        duration_months=request.duration_months
    )
    
    return handler.handle_create_loan(command)
