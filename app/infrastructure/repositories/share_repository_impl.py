"""Share repository implementation."""
from typing import Optional, List
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.domain.repositories.share_repository import IShareRepository
from app.domain.entities.share import Share
from app.infrastructure.database.models import ShareModel


class ShareRepository(IShareRepository):
    """SQLAlchemy implementation of Share repository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: ShareModel) -> Share:
        """Convert database model to domain entity."""
        return Share(
            id=model.id,
            user_id=model.user_id,
            shares_count=model.shares_count,
            share_value=Decimal(str(model.share_value)),
            total_value=Decimal(str(model.total_value)),
            purchase_date=model.purchase_date,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, entity: Share) -> ShareModel:
        """Convert domain entity to database model."""
        return ShareModel(
            id=entity.id,
            user_id=entity.user_id,
            shares_count=entity.shares_count,
            share_value=entity.share_value,
            total_value=entity.total_value,
            purchase_date=entity.purchase_date,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    def create(self, share: Share) -> Share:
        """Create a new share record."""
        db_share = self._to_model(share)
        self.db.add(db_share)
        self.db.commit()
        self.db.refresh(db_share)
        return self._to_entity(db_share)
    
    def get_by_id(self, share_id: int) -> Optional[Share]:
        """Get share by ID."""
        db_share = self.db.query(ShareModel).filter(ShareModel.id == share_id).first()
        return self._to_entity(db_share) if db_share else None
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Share]:
        """Get all shares for a user."""
        db_shares = self.db.query(ShareModel).filter(
            ShareModel.user_id == user_id
        ).offset(skip).limit(limit).all()
        return [self._to_entity(s) for s in db_shares]
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Share]:
        """Get all shares with pagination."""
        db_shares = self.db.query(ShareModel).offset(skip).limit(limit).all()
        return [self._to_entity(s) for s in db_shares]
    
    def update(self, share: Share) -> Share:
        """Update share record."""
        db_share = self.db.query(ShareModel).filter(ShareModel.id == share.id).first()
        if db_share:
            db_share.user_id = share.user_id
            db_share.shares_count = share.shares_count
            db_share.share_value = share.share_value
            db_share.total_value = share.total_value
            db_share.purchase_date = share.purchase_date
            db_share.updated_at = share.updated_at
            self.db.commit()
            self.db.refresh(db_share)
            return self._to_entity(db_share)
        return share
    
    def delete(self, share_id: int) -> bool:
        """Delete share record."""
        db_share = self.db.query(ShareModel).filter(ShareModel.id == share_id).first()
        if db_share:
            self.db.delete(db_share)
            self.db.commit()
            return True
        return False
    
    def get_total_shares_by_user(self, user_id: int) -> int:
        """Get total number of shares for a user."""
        result = self.db.query(func.sum(ShareModel.shares_count)).filter(
            ShareModel.user_id == user_id
        ).scalar()
        return int(result) if result else 0
    
    def get_total_value_by_user(self, user_id: int) -> Decimal:
        """Get total value of shares for a user."""
        result = self.db.query(func.sum(ShareModel.total_value)).filter(
            ShareModel.user_id == user_id
        ).scalar()
        return Decimal(str(result)) if result else Decimal("0.00")
    
    def get_total_value_all_users(self) -> Decimal:
        """Get total value of shares for all users."""
        result = self.db.query(func.sum(ShareModel.total_value)).scalar()
        return Decimal(str(result)) if result else Decimal("0.00")
