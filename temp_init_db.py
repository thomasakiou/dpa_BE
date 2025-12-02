"""Temporary database initialization using alembic.ini credentials."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database.base import Base
from app.infrastructure.database.models import UserModel
from app.domain.entities.user import UserRole, UserStatus
from app.core.security import get_password_hash

# Use the credentials from alembic.ini
DATABASE_URL = "postgresql://postgres:ebimobowei81@localhost:5432/dpa_db"

# Create engine with the alembic.ini credentials
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")

def init_db(db):
    """Initialize database with default admin user."""
    # Check if admin user already exists
    admin_user = db.query(UserModel).filter(
        UserModel.email == "admin@dpa.com"
    ).first()
    
    if not admin_user:
        # Create default admin user
        admin_user = UserModel(
            member_id="DPA001",
            email="admin@dpa.com",
            hashed_password=get_password_hash("admin123"),
            full_name="System Administrator",
            phone="",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        db.add(admin_user)
        db.commit()
        print(f"✓ Created default admin user: admin@dpa.com")
    else:
        print(f"✓ Admin user already exists: admin@dpa.com")

if __name__ == "__main__":
    print("Initializing database with alembic.ini credentials...")
    print(f"Database URL: {DATABASE_URL.replace('ebimobowei81', '***')}")
    
    try:
        create_tables()
        
        db = SessionLocal()
        try:
            init_db(db)
            print("✓ Database initialization completed successfully")
        finally:
            db.close()
    except Exception as e:
        print(f"✗ Error: {e}")
        raise
