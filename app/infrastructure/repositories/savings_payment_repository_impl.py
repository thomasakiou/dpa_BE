"""Savings payment repository implementation."""
from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.domain.repositories.savings_payment_repository import ISavingsPaymentRepository
from app.domain.entities.savings_payment import SavingsPayment, SavingsPaymentType
from app.infrastructure.database.models import SavingsPaymentModel


class SavingsPaymentRepository(ISavingsPaymentRepository):
    """SQLAlchemy implementation of savings payment repository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, payment: SavingsPayment) -> SavingsPayment:
        """Create a new savings payment record."""
        db_payment = SavingsPaymentModel(
            user_id=payment.user_id,
            amount=payment.amount,
            type=payment.type,
            payment_date=payment.payment_date,
            payment_month=payment.payment_month,
            description=payment.description
        )
        
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        
        return self._to_entity(db_payment)
    
    def get_by_id(self, payment_id: int) -> Optional[SavingsPayment]:
        """Get a savings payment by ID."""
        db_payment = self.db.query(SavingsPaymentModel).filter(
            SavingsPaymentModel.id == payment_id
        ).first()
        
        return self._to_entity(db_payment) if db_payment else None
    
    def get_all(self, skip: int = 0, limit: Optional[int] = None) -> List[SavingsPayment]:
        """Get all savings payment records with pagination. No limit by default."""
        query = self.db.query(SavingsPaymentModel).offset(skip)
        
        if limit is not None:
            query = query.limit(limit)
        
        db_payments = query.all()
        return [self._to_entity(p) for p in db_payments]
    
    def update(self, payment: SavingsPayment) -> SavingsPayment:
        """Update an existing savings payment record."""
        db_payment = self.db.query(SavingsPaymentModel).filter(
            SavingsPaymentModel.id == payment.id
        ).first()
        
        if not db_payment:
            raise ValueError(f"Savings payment with id {payment.id} not found")
        
        db_payment.user_id = payment.user_id
        db_payment.amount = payment.amount
        db_payment.type = payment.type
        db_payment.payment_date = payment.payment_date
        db_payment.payment_month = payment.payment_month
        db_payment.description = payment.description
        
        self.db.commit()
        self.db.refresh(db_payment)
        
        return self._to_entity(db_payment)
    
    def delete(self, payment_id: int) -> bool:
        """Delete a savings payment record."""
        db_payment = self.db.query(SavingsPaymentModel).filter(
            SavingsPaymentModel.id == payment_id
        ).first()
        
        if not db_payment:
            return False
        
        self.db.delete(db_payment)
        self.db.commit()
        
        return True
    
    def _to_entity(self, model: SavingsPaymentModel) -> SavingsPayment:
        """Convert database model to domain entity."""
        return SavingsPayment(
            id=model.id,
            user_id=model.user_id,
            amount=model.amount,
            type=model.type,
            payment_date=model.payment_date,
            payment_month=model.payment_month,
            description=model.description,
            created_at=model.created_at
        )

    def get_by_user(self, user_id: int, skip: int = 0, limit: Optional[int] = None) -> List[SavingsPayment]:
        """Get all savings payments for a specific user. No limit by default."""
        query = self.db.query(SavingsPaymentModel).filter(
            SavingsPaymentModel.user_id == user_id
        ).offset(skip)
        
        if limit is not None:
            query = query.limit(limit)
        
        db_payments = query.all()
        return [self._to_entity(p) for p in db_payments]

    def get_total_paid_by_user(self, user_id: int) -> Decimal:
        """Get total amount paid by a user."""
        result = self.db.query(func.sum(SavingsPaymentModel.amount)).filter(
            SavingsPaymentModel.user_id == user_id
        ).scalar()
        return Decimal(str(result)) if result else Decimal("0.00")

    def get_count_by_user(self, user_id: int) -> int:
        """Get total count of payments for a user."""
        return self.db.query(SavingsPaymentModel).filter(
            SavingsPaymentModel.user_id == user_id
        ).count()
