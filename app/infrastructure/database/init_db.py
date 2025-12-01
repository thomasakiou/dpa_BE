"""Database initialization script."""
from sqlalchemy.orm import Session
from app.infrastructure.database.base import engine, Base
from app.infrastructure.database.models import UserModel
from app.domain.entities.user import UserRole, UserStatus
from app.core.security import get_password_hash
from app.core.config import settings


def init_db(db: Session) -> None:
    """Initialize database with default data."""
    # Check if admin user already exists
    admin_user = db.query(UserModel).filter(
        UserModel.email == settings.DEFAULT_ADMIN_EMAIL
    ).first()
    
    if not admin_user:
        # Create default admin user
        admin_user = UserModel(
            member_id=settings.DEFAULT_ADMIN_MEMBER_ID,
            email=settings.DEFAULT_ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),
            full_name="System Administrator",
            phone="",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        db.add(admin_user)
        db.commit()
        print(f"✓ Created default admin user: {settings.DEFAULT_ADMIN_EMAIL}")
    else:
        print(f"✓ Admin user already exists: {settings.DEFAULT_ADMIN_EMAIL}")


def create_tables() -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")


if __name__ == "__main__":
    from app.infrastructure.database.session import SessionLocal
    
    print("Initializing database...")
    create_tables()
    
    db = SessionLocal()
    try:
        init_db(db)
        print("✓ Database initialization completed successfully")
    finally:
        db.close()
