"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum as SQLEnum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.base import Base
from app.domain.entities.user import UserRole, UserStatus
from app.domain.entities.savings import SavingsStatus
from app.domain.entities.loan import LoanStatus
from app.domain.entities.transaction import TransactionType
from app.domain.entities.savings_payment import SavingsPaymentType


class UserModel(Base):
    """SQLAlchemy model for User entity."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    role = Column(SQLEnum(UserRole), default=UserRole.MEMBER, nullable=False)
    status = Column(SQLEnum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    savings = relationship("SavingsModel", back_populates="user", cascade="all, delete-orphan")
    savings_payments = relationship("SavingsPaymentModel", back_populates="user", cascade="all, delete-orphan")
    shares = relationship("ShareModel", back_populates="user", cascade="all, delete-orphan")
    loans = relationship("LoanModel", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("TransactionModel", back_populates="user", cascade="all, delete-orphan")


class SavingsModel(Base):
    """SQLAlchemy model for Savings entity."""
    __tablename__ = "savings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    expected_amount = Column(Numeric(10, 2), nullable=False)
    paid_amount = Column(Numeric(10, 2), default=0.00)
    status = Column(SQLEnum(SavingsStatus), default=SavingsStatus.PENDING, nullable=False)
    payment_date = Column(DateTime(timezone=True))
    financial_year = Column(String(9), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="savings")


class SavingsPaymentModel(Base):
    """SQLAlchemy model for Savings Payment entity."""
    __tablename__ = "savings_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(SQLEnum(SavingsPaymentType), nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False)
    payment_month = Column(String(20), nullable=True)
    financial_year = Column(String(9), nullable=True, index=True)
    description = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="savings_payments")


class ShareModel(Base):
    """SQLAlchemy model for Share entity."""
    __tablename__ = "shares"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shares_count = Column(Integer, default=0)
    share_value = Column(Numeric(10, 2), nullable=False)
    total_value = Column(Numeric(10, 2), nullable=False)
    purchase_date = Column(DateTime(timezone=True), server_default=func.now())
    financial_year = Column(String(9), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="shares")


class LoanModel(Base):
    """SQLAlchemy model for Loan entity."""
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    loan_amount = Column(Numeric(10, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), nullable=False)
    duration_months = Column(Integer, nullable=False)
    monthly_repayment = Column(Numeric(10, 2), nullable=False)
    total_repayable = Column(Numeric(10, 2), nullable=False)
    amount_paid = Column(Numeric(10, 2), default=0.00)
    balance = Column(Numeric(10, 2), nullable=False)
    status = Column(SQLEnum(LoanStatus), default=LoanStatus.PENDING, nullable=False)
    application_date = Column(DateTime(timezone=True), server_default=func.now())
    approval_date = Column(DateTime(timezone=True))
    disbursement_date = Column(DateTime(timezone=True))
    financial_year = Column(String(9), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="loans")


class TransactionModel(Base):
    """SQLAlchemy model for Transaction entity."""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    description = Column(String(500), nullable=False)
    debit = Column(Numeric(10, 2), default=0.00)
    credit = Column(Numeric(10, 2), default=0.00)
    balance = Column(Numeric(10, 2), nullable=False)
    reference_id = Column(Integer)
    financial_year = Column(String(9), nullable=True, index=True)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="transactions")


class SystemSettingsModel(Base):
    """SQLAlchemy model for System Settings."""
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(String(500), nullable=False)
    description = Column(String(500))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

