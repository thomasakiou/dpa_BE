"""Admin API routes."""
import secrets
import string
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, require_admin
from app.infrastructure.repositories.user_repository_impl import UserRepository
from app.infrastructure.repositories.loan_repository_impl import LoanRepository
from app.infrastructure.repositories.savings_payment_repository_impl import SavingsPaymentRepository
from app.infrastructure.repositories.share_repository_impl import ShareRepository
from app.application.handlers.user_handlers import UserHandler
from app.application.handlers.loan_handlers import LoanHandler
from app.application.handlers.savings_payment_handlers import SavingsPaymentHandler
from app.application.handlers.share_handlers import ShareHandler
from app.application.queries.queries import GetUsersQuery, GetAllLoansQuery, GetAllSavingsPaymentsQuery, GetAllSharesQuery
from app.application.commands.user_commands import CreateUserCommand, SuspendUserCommand, ActivateUserCommand, UpdateUserCommand, ResetPasswordCommand
from app.application.commands.loan_commands import CloseLoanCommand, ApproveLoanCommand, DeleteLoanCommand, RecordLoanRepaymentCommand, DisburseLoanCommand
from app.application.commands.savings_payment_commands import CreateSavingsPaymentCommand, UpdateSavingsPaymentCommand, DeleteSavingsPaymentCommand
from app.application.commands.share_commands import CreateShareCommand, UpdateShareCommand, DeleteShareCommand
from app.presentation.schemas.user import UserResponse, UserCreate, UserUpdate, PasswordResetResponse
from app.presentation.schemas.loan import LoanResponse, LoanRepayment
from app.presentation.schemas.savings_payment import SavingsPaymentResponse, SavingsPaymentCreate, SavingsPaymentUpdate
from app.presentation.schemas.share import ShareResponse, ShareCreate, ShareUpdate

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
    db: Session = Depends(get_db)
):
    """Get all users (admin only). Returns all records without pagination."""
    user_repo = UserRepository(db)
    handler = UserHandler(user_repo)
    
    query = GetUsersQuery(skip=0, limit=None)
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


@router.put("/users/{user_id}", response_model=UserResponse, dependencies=[Depends(require_admin)])
def update_user(
    user_id: int,
    request: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update a user (admin only)."""
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


@router.post("/users/{user_id}/reset-password", response_model=PasswordResetResponse, dependencies=[Depends(require_admin)])
def reset_user_password(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Reset a user's password (admin only)."""
    # Use fixed password as requested
    new_password = "12345678"
    
    user_repo = UserRepository(db)
    handler = UserHandler(user_repo)
    
    command = ResetPasswordCommand(user_id=user_id, new_password=new_password)
    handler.handle_reset_password(command)
    
    return PasswordResetResponse(
        new_password=new_password,
        message="Password reset successfully"
    )




@router.get("/loans", response_model=List[LoanResponse], dependencies=[Depends(require_admin)])
def get_all_loans(
    db: Session = Depends(get_db)
):
    """Get all loans (admin only). Returns all records without pagination."""
    loan_repo = LoanRepository(db)
    handler = LoanHandler(loan_repo)
    
    query = GetAllLoansQuery(skip=0, limit=None)
    return handler.handle_get_all_loans(query)


@router.post("/loans/{loan_id}/close", response_model=LoanResponse, dependencies=[Depends(require_admin)])
def close_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    """Close/payoff a loan (admin only)."""
    loan_repo = LoanRepository(db)
    handler = LoanHandler(loan_repo)
    
    command = CloseLoanCommand(loan_id=loan_id)
    return handler.handle_close_loan(command)


@router.post("/loans/{loan_id}/approve", response_model=LoanResponse, dependencies=[Depends(require_admin)])
def approve_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    """Approve a pending loan (admin only)."""
    loan_repo = LoanRepository(db)
    handler = LoanHandler(loan_repo)
    
    command = ApproveLoanCommand(loan_id=loan_id)
    return handler.handle_approve_loan(command)


@router.post("/loans/{loan_id}/disburse", response_model=LoanResponse, dependencies=[Depends(require_admin)])
def disburse_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    """Disburse/activate an approved loan (admin only)."""
    loan_repo = LoanRepository(db)
    handler = LoanHandler(loan_repo)
    
    command = DisburseLoanCommand(loan_id=loan_id)
    return handler.handle_disburse_loan(command)


@router.delete("/loans/{loan_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    """Delete a loan (admin only)."""
    loan_repo = LoanRepository(db)
    handler = LoanHandler(loan_repo)
    
    command = DeleteLoanCommand(loan_id=loan_id)
    handler.handle_delete_loan(command)
    return None


@router.post("/loans/{loan_id}/payment", response_model=LoanResponse, dependencies=[Depends(require_admin)])
def record_loan_payment(
    loan_id: int,
    request: LoanRepayment,
    db: Session = Depends(get_db)
):
    """Record a partial loan payment (admin only)."""
    loan_repo = LoanRepository(db)
    handler = LoanHandler(loan_repo)
    
    command = RecordLoanRepaymentCommand(
        loan_id=loan_id,
        amount=request.amount
    )
    return handler.handle_record_repayment(command)


@router.get("/savings", response_model=List[SavingsPaymentResponse], dependencies=[Depends(require_admin)])
def get_all_savings_payments(
    db: Session = Depends(get_db)
):
    """Get all savings payment records (admin only). Returns all records without pagination."""
    repo = SavingsPaymentRepository(db)
    handler = SavingsPaymentHandler(repo)
    
    query = GetAllSavingsPaymentsQuery(skip=0, limit=None)
    return handler.handle_get_all_payments(query)


@router.post("/savings", response_model=SavingsPaymentResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_savings_payment(
    request: SavingsPaymentCreate,
    db: Session = Depends(get_db)
):
    """Create a new savings payment record (admin only)."""
    repo = SavingsPaymentRepository(db)
    handler = SavingsPaymentHandler(repo)
    
    command = CreateSavingsPaymentCommand(
        user_id=request.user_id,
        amount=request.amount,
        type=request.type.value,
        payment_date=request.payment_date,
        payment_month=request.payment_month,
        description=request.description
    )
    
    return handler.handle_create_payment(command)


@router.put("/savings/{payment_id}", response_model=SavingsPaymentResponse, dependencies=[Depends(require_admin)])
def update_savings_payment(
    payment_id: int,
    request: SavingsPaymentUpdate,
    db: Session = Depends(get_db)
):
    """Update a savings payment record (admin only)."""
    repo = SavingsPaymentRepository(db)
    handler = SavingsPaymentHandler(repo)
    
    command = UpdateSavingsPaymentCommand(
        payment_id=payment_id,
        amount=request.amount,
        type=request.type.value if request.type else None,
        payment_date=request.payment_date,
        payment_month=request.payment_month,
        description=request.description
    )
    
    return handler.handle_update_payment(command)


@router.delete("/savings/{payment_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_savings_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    """Delete a savings payment record (admin only)."""
    repo = SavingsPaymentRepository(db)
    handler = SavingsPaymentHandler(repo)
    
    command = DeleteSavingsPaymentCommand(payment_id=payment_id)
    handler.handle_delete_payment(command)
    return None


@router.get("/shares", response_model=List[ShareResponse], dependencies=[Depends(require_admin)])
def get_all_shares(
    db: Session = Depends(get_db)
):
    """Get all shares (admin only). Returns all records without pagination."""
    share_repo = ShareRepository(db)
    handler = ShareHandler(share_repo)
    
    query = GetAllSharesQuery(skip=0, limit=None)
    return handler.handle_get_all_shares(query)


@router.post("/shares", response_model=ShareResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_share(
    request: ShareCreate,
    db: Session = Depends(get_db)
):
    """Create a new share record (admin only)."""
    share_repo = ShareRepository(db)
    handler = ShareHandler(share_repo)
    
    command = CreateShareCommand(
        user_id=request.user_id,
        shares_count=request.shares_count,
        share_value=request.share_value,
        purchase_date=request.purchase_date
    )
    
    return handler.handle_create_share(command)


@router.put("/shares/{share_id}", response_model=ShareResponse, dependencies=[Depends(require_admin)])
def update_share(
    share_id: int,
    request: ShareUpdate,
    db: Session = Depends(get_db)
):
    """Update a share record (admin only)."""
    share_repo = ShareRepository(db)
    handler = ShareHandler(share_repo)
    
    command = UpdateShareCommand(
        share_id=share_id,
        shares_count=request.shares_count,
        share_value=request.share_value
    )
    
    return handler.handle_update_share(command)


@router.delete("/shares/{share_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_share(
    share_id: int,
    db: Session = Depends(get_db)
):
    """Delete a share record (admin only)."""
    share_repo = ShareRepository(db)
    handler = ShareHandler(share_repo)
    
    command = DeleteShareCommand(share_id=share_id)
    handler.handle_delete_share(command)
    return None


