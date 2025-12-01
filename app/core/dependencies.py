"""Dependency injection for database sessions and authentication."""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.infrastructure.database.session import SessionLocal
from app.core.security import decode_access_token
from app.domain.entities.user import UserRole


# HTTP Bearer token security scheme
security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    Dependency to get current authenticated user ID from JWT token.
    
    Args:
        credentials: HTTP Authorization credentials containing JWT token
        
    Returns:
        User ID from token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return int(user_id)


def get_current_user_role(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependency to get current authenticated user's role from JWT token.
    
    Args:
        credentials: HTTP Authorization credentials containing JWT token
        
    Returns:
        User role from token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    role: Optional[str] = payload.get("role")
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return role


def require_admin(role: str = Depends(get_current_user_role)) -> None:
    """
    Dependency to require admin role.
    
    Args:
        role: User role from token
        
    Raises:
        HTTPException: If user is not an admin
    """
    if role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin access required."
        )


def require_member_or_admin(role: str = Depends(get_current_user_role)) -> None:
    """
    Dependency to require member or admin role.
    
    Args:
        role: User role from token
        
    Raises:
        HTTPException: If user role is invalid
    """
    if role not in [UserRole.ADMIN.value, UserRole.MEMBER.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions."
        )
