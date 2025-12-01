"""Query models for retrieving data."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GetUserQuery(BaseModel):
    """Query to get user by ID."""
    user_id: int


class GetUsersQuery(BaseModel):
    """Query to get all users with pagination."""
    skip: int = 0
    limit: int = 100


class GetUserDashboardQuery(BaseModel):
    """Query to get user dashboard data."""
    user_id: int


class GetUserSavingsQuery(BaseModel):
    """Query to get user savings."""
    user_id: int
    skip: int = 0
    limit: int = 100


class GetUserSharesQuery(BaseModel):
    """Query to get user shares."""
    user_id: int
    skip: int = 0
    limit: int = 100


class GetUserLoansQuery(BaseModel):
    """Query to get user loans."""
    user_id: int
    skip: int = 0
    limit: int = 100


class GetUserStatementQuery(BaseModel):
    """Query to get user statement."""
    user_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    skip: int = 0
    limit: int = 100


class GetAdminDashboardQuery(BaseModel):
    """Query to get admin dashboard data."""
    pass


class GetAllSavingsQuery(BaseModel):
    """Query to get all savings with pagination."""
    skip: int = 0
    limit: int = 100


class GetAllSharesQuery(BaseModel):
    """Query to get all shares with pagination."""
    skip: int = 0
    limit: int = 100


class GetAllLoansQuery(BaseModel):
    """Query to get all loans with pagination."""
    skip: int = 0
    limit: int = 100
