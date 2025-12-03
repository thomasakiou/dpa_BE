"""Savings repository implementation."""
from typing import Optional, List
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.domain.repositories.savings_repository import ISavingsRepository
from app.domain.entities.savings import Savings, SavingsStatus
from app.infrastructure.database.models import SavingsModel


class SavingsRepository(ISavingsRepository):
    """SQLAlchemy implementation of Savings repository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: SavingsModel) -> Savings:
        """Convert database model to domain entity."""
        return Savings(
            id=model.id,
            user_id=model.user_id,
            month=model.month,
            year=model.year,
            expected_amount=Decimal(str(model.expected_amount)),
            paid_amount=Decimal(str(model.paid_amount)),
            status=model.status,
            payment_date=model.payment_date,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, entity: Savings) -> SavingsModel:
        """Convert domain entity to database model."""
        return SavingsModel(
            id=entity.id,
            user_id=entity.user_id,
            month=entity.month,
            year=entity.year,
            expected_amount=entity.expected_amount,
            paid_amount=entity.paid_amount,
            status=entity.status,
            payment_date=entity.payment_date,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    def create(self, savings: Savings) -> Savings:
        """Create a new savings record."""
        db_savings = self._to_model(savings)
        self.db.add(db_savings)
        self.db.commit()
        self.db.refresh(db_savings)
        return self._to_entity(db_savings)
    
    def get_by_id(self, savings_id: int) -> Optional[Savings]:
        """Get savings by ID."""
        db_savings = self.db.query(SavingsModel).filter(SavingsModel.id == savings_id).first()
        return self._to_entity(db_savings) if db_savings else None
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Savings]:
        """Get all savings for a user."""
        db_savings = self.db.query(SavingsModel).filter(
            SavingsModel.user_id == user_id
        ).offset(skip).limit(limit).all()
        return [self._to_entity(s) for s in db_savings]
    
    def get_by_user_and_period(self, user_id: int, month: str, year: int) -> Optional[Savings]:
        """Get savings for a specific month and year."""
        db_savings = self.db.query(SavingsModel).filter(
            SavingsModel.user_id == user_id,
            SavingsModel.month == month,
            SavingsModel.year == year
        ).first()
        return self._to_entity(db_savings) if db_savings else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Savings]:
        """Get all savings with pagination."""
        db_savings = self.db.query(SavingsModel).offset(skip).limit(limit).all()
        return [self._to_entity(s) for s in db_savings]
    
    def update(self, savings: Savings) -> Savings:
        """Update savings record."""
        db_savings = self.db.query(SavingsModel).filter(SavingsModel.id == savings.id).first()
        if db_savings:
            db_savings.user_id = savings.user_id
            db_savings.month = savings.month
            db_savings.year = savings.year
            db_savings.expected_amount = savings.expected_amount
            db_savings.paid_amount = savings.paid_amount
            db_savings.status = savings.status
            db_savings.payment_date = savings.payment_date
            db_savings.updated_at = savings.updated_at
            self.db.commit()
            self.db.refresh(db_savings)
            return self._to_entity(db_savings)
        return savings
    
    def delete(self, savings_id: int) -> bool:
        """Delete savings record."""
        db_savings = self.db.query(SavingsModel).filter(SavingsModel.id == savings_id).first()
        if db_savings:
            self.db.delete(db_savings)
            self.db.commit()
            return True
        return False
    
    def get_total_by_user(self, user_id: int) -> Decimal:
        """Get total savings amount for a user."""
        result = self.db.query(func.sum(SavingsModel.paid_amount)).filter(
            SavingsModel.user_id == user_id
        ).scalar()
        return Decimal(str(result)) if result else Decimal("0.00")
    
    def get_total_all_users(self) -> Decimal:
        """Get total savings amount for all users."""
        result = self.db.query(func.sum(SavingsModel.paid_amount)).scalar()
        return Decimal(str(result)) if result else Decimal("0.00")

    def get_total_expected_by_user(self, user_id: int) -> Decimal:
        """Get total expected savings amount for a user."""
        result = self.db.query(func.sum(SavingsModel.expected_amount)).filter(
            SavingsModel.user_id == user_id
        ).scalar()
        return Decimal(str(result)) if result else Decimal("0.00")
