"""Transaction repository implementation."""
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from app.domain.repositories.transaction_repository import ITransactionRepository
from app.domain.entities.transaction import Transaction, TransactionType
from app.infrastructure.database.models import TransactionModel


class TransactionRepository(ITransactionRepository):
    """SQLAlchemy implementation of Transaction repository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: TransactionModel) -> Transaction:
        """Convert database model to domain entity."""
        return Transaction(
            id=model.id,
            user_id=model.user_id,
            transaction_type=model.transaction_type,
            description=model.description,
            debit=Decimal(str(model.debit)),
            credit=Decimal(str(model.credit)),
            balance=Decimal(str(model.balance)),
            reference_id=model.reference_id,
            transaction_date=model.transaction_date,
            created_at=model.created_at
        )
    
    def _to_model(self, entity: Transaction) -> TransactionModel:
        """Convert domain entity to database model."""
        return TransactionModel(
            id=entity.id,
            user_id=entity.user_id,
            transaction_type=entity.transaction_type,
            description=entity.description,
            debit=entity.debit,
            credit=entity.credit,
            balance=entity.balance,
            reference_id=entity.reference_id,
            transaction_date=entity.transaction_date,
            created_at=entity.created_at
        )
    
    def create(self, transaction: Transaction) -> Transaction:
        """Create a new transaction."""
        db_transaction = self._to_model(transaction)
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return self._to_entity(db_transaction)
    
    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID."""
        db_transaction = self.db.query(TransactionModel).filter(
            TransactionModel.id == transaction_id
        ).first()
        return self._to_entity(db_transaction) if db_transaction else None
    
    def get_by_user(
        self, 
        user_id: int, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Transaction]:
        """Get transactions for a user with optional date filtering."""
        query = self.db.query(TransactionModel).filter(TransactionModel.user_id == user_id)
        
        if start_date:
            query = query.filter(TransactionModel.transaction_date >= start_date)
        if end_date:
            query = query.filter(TransactionModel.transaction_date <= end_date)
        
        db_transactions = query.order_by(
            TransactionModel.transaction_date.desc()
        ).offset(skip).limit(limit).all()
        
        return [self._to_entity(t) for t in db_transactions]
    
    def get_by_type(
        self, 
        transaction_type: TransactionType,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Transaction]:
        """Get transactions by type."""
        db_transactions = self.db.query(TransactionModel).filter(
            TransactionModel.transaction_type == transaction_type
        ).offset(skip).limit(limit).all()
        return [self._to_entity(t) for t in db_transactions]
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Transaction]:
        """Get all transactions with pagination."""
        db_transactions = self.db.query(TransactionModel).order_by(
            TransactionModel.transaction_date.desc()
        ).offset(skip).limit(limit).all()
        return [self._to_entity(t) for t in db_transactions]
