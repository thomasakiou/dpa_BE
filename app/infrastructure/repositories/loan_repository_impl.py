"""Loan repository implementation."""
from typing import Optional, List
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.domain.repositories.loan_repository import ILoanRepository
from app.domain.entities.loan import Loan, LoanStatus
from app.infrastructure.database.models import LoanModel


class LoanRepository(ILoanRepository):
    """SQLAlchemy implementation of Loan repository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: LoanModel) -> Loan:
        """Convert database model to domain entity."""
        return Loan(
            id=model.id,
            user_id=model.user_id,
            loan_amount=Decimal(str(model.loan_amount)),
            interest_rate=Decimal(str(model.interest_rate)),
            duration_months=model.duration_months,
            monthly_repayment=Decimal(str(model.monthly_repayment)),
            total_repayable=Decimal(str(model.total_repayable)),
            amount_paid=Decimal(str(model.amount_paid)),
            balance=Decimal(str(model.balance)),
            status=model.status,
            application_date=model.application_date,
            approval_date=model.approval_date,
            disbursement_date=model.disbursement_date,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, entity: Loan) -> LoanModel:
        """Convert domain entity to database model."""
        return LoanModel(
            id=entity.id,
            user_id=entity.user_id,
            loan_amount=entity.loan_amount,
            interest_rate=entity.interest_rate,
            duration_months=entity.duration_months,
            monthly_repayment=entity.monthly_repayment,
            total_repayable=entity.total_repayable,
            amount_paid=entity.amount_paid,
            balance=entity.balance,
            status=entity.status,
            application_date=entity.application_date,
            approval_date=entity.approval_date,
            disbursement_date=entity.disbursement_date,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    def create(self, loan: Loan) -> Loan:
        """Create a new loan."""
        db_loan = self._to_model(loan)
        self.db.add(db_loan)
        self.db.commit()
        self.db.refresh(db_loan)
        return self._to_entity(db_loan)
    
    def get_by_id(self, loan_id: int) -> Optional[Loan]:
        """Get loan by ID."""
        db_loan = self.db.query(LoanModel).filter(LoanModel.id == loan_id).first()
        return self._to_entity(db_loan) if db_loan else None
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Loan]:
        """Get all loans for a user."""
        db_loans = self.db.query(LoanModel).filter(
            LoanModel.user_id == user_id
        ).offset(skip).limit(limit).all()
        return [self._to_entity(loan) for loan in db_loans]
    
    def get_by_status(self, status: LoanStatus, skip: int = 0, limit: int = 100) -> List[Loan]:
        """Get loans by status."""
        db_loans = self.db.query(LoanModel).filter(
            LoanModel.status == status
        ).offset(skip).limit(limit).all()
        return [self._to_entity(loan) for loan in db_loans]
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Loan]:
        """Get all loans with pagination."""
        db_loans = self.db.query(LoanModel).offset(skip).limit(limit).all()
        return [self._to_entity(loan) for loan in db_loans]
    
    def update(self, loan: Loan) -> Loan:
        """Update loan."""
        db_loan = self.db.query(LoanModel).filter(LoanModel.id == loan.id).first()
        if db_loan:
            db_loan.user_id = loan.user_id
            db_loan.loan_amount = loan.loan_amount
            db_loan.interest_rate = loan.interest_rate
            db_loan.duration_months = loan.duration_months
            db_loan.monthly_repayment = loan.monthly_repayment
            db_loan.total_repayable = loan.total_repayable
            db_loan.amount_paid = loan.amount_paid
            db_loan.balance = loan.balance
            db_loan.status = loan.status
            db_loan.application_date = loan.application_date
            db_loan.approval_date = loan.approval_date
            db_loan.disbursement_date = loan.disbursement_date
            db_loan.updated_at = loan.updated_at
            self.db.commit()
            self.db.refresh(db_loan)
            return self._to_entity(db_loan)
        return loan
    
    def delete(self, loan_id: int) -> bool:
        """Delete loan."""
        db_loan = self.db.query(LoanModel).filter(LoanModel.id == loan_id).first()
        if db_loan:
            self.db.delete(db_loan)
            self.db.commit()
            return True
        return False
    
    def get_total_disbursed(self) -> Decimal:
        """Get total amount of disbursed loans."""
        result = self.db.query(func.sum(LoanModel.loan_amount)).filter(
            LoanModel.status.in_([LoanStatus.ACTIVE, LoanStatus.CLOSED])
        ).scalar()
        return Decimal(str(result)) if result else Decimal("0.00")
    
    def get_total_outstanding(self) -> Decimal:
        """Get total outstanding loan balance."""
        result = self.db.query(func.sum(LoanModel.balance)).filter(
            LoanModel.status == LoanStatus.ACTIVE
        ).scalar()
        return Decimal(str(result)) if result else Decimal("0.00")
    
    def get_user_active_loans(self, user_id: int) -> List[Loan]:
        """Get active loans for a user."""
        db_loans = self.db.query(LoanModel).filter(
            LoanModel.user_id == user_id,
            LoanModel.status == LoanStatus.ACTIVE
        ).all()
        return [self._to_entity(loan) for loan in db_loans]
