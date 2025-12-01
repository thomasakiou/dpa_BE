"""API v1 router configuration."""
from fastapi import APIRouter
from app.presentation.api.v1 import auth, members, savings, shares, loans, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(members.router, prefix="/members", tags=["Members"])
api_router.include_router(savings.router, prefix="/savings", tags=["Savings"])
api_router.include_router(shares.router, prefix="/shares", tags=["Shares"])
api_router.include_router(loans.router, prefix="/loans", tags=["Loans"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
