"""
User routes — protected endpoints for user account management.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.user_service import (
    get_all_users,
    create_user,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all user accounts (protected route)."""
    return get_all_users(db)


@router.post("/", response_model=UserOut, status_code=201)
def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new user account (protected route)."""
    return create_user(db, user_data)


@router.put("/{user_id}", response_model=UserOut)
def update_existing_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a user's username or password (protected route)."""
    return update_user(db, user_id, user_data)


@router.delete("/{user_id}")
def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a user account (protected route)."""
    return delete_user(db, user_id)
