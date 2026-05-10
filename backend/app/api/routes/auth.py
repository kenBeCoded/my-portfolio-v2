"""
Authentication routes — register, login, logout, and session check.
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import Token
from app.services.auth_service import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account."""
    return register_user(db, user_data)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authenticate user and return a JWT access token (4-hour expiry)."""
    return authenticate_user(db, form_data.username, form_data.password)


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """Logout the current user (client should discard the token)."""
    return {"detail": "Successfully logged out"}


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """Validate current session and return the authenticated user."""
    return current_user
