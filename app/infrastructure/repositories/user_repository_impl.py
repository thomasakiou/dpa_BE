"""User repository implementation."""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.repositories.user_repository import IUserRepository
from app.domain.entities.user import User, UserRole, UserStatus
from app.infrastructure.database.models import UserModel


class UserRepository(IUserRepository):
    """SQLAlchemy implementation of User repository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: UserModel) -> User:
        """Convert database model to domain entity."""
        return User(
            id=model.id,
            member_id=model.member_id,
            email=model.email,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            phone=model.phone,
            role=model.role,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, entity: User) -> UserModel:
        """Convert domain entity to database model."""
        return UserModel(
            id=entity.id,
            member_id=entity.member_id,
            email=entity.email,
            hashed_password=entity.hashed_password,
            full_name=entity.full_name,
            phone=entity.phone,
            role=entity.role,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    def create(self, user: User) -> User:
        """Create a new user."""
        db_user = self._to_model(user)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(db_user) if db_user else None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(db_user) if db_user else None
    
    def get_by_member_id(self, member_id: str) -> Optional[User]:
        """Get user by member ID."""
        db_user = self.db.query(UserModel).filter(UserModel.member_id == member_id).first()
        return self._to_entity(db_user) if db_user else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        db_users = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [self._to_entity(user) for user in db_users]
    
    def update(self, user: User) -> User:
        """Update user."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if db_user:
            db_user.member_id = user.member_id
            db_user.email = user.email
            db_user.hashed_password = user.hashed_password
            db_user.full_name = user.full_name
            db_user.phone = user.phone
            db_user.role = user.role
            db_user.status = user.status
            db_user.updated_at = user.updated_at
            self.db.commit()
            self.db.refresh(db_user)
            return self._to_entity(db_user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        """Count total users."""
        return self.db.query(UserModel).count()
