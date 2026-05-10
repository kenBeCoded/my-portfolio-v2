"""
User service — business logic for CRUD operations on user accounts.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.hash import hash_password


def get_all_users(db: Session) -> list[User]:
    """Return all user accounts."""
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int) -> User:
    """Return a single user by ID.

    Raises:
        HTTPException 404 if user not found.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user account.

    Raises:
        HTTPException 400 if username already exists.
    """
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    new_user = User(
        username=user_data.username,
        password=hash_password(user_data.password),
        fullname=user_data.fullname,
        role=user_data.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    """Update an existing user's username or password.

    Raises:
        HTTPException 404 if user not found.
        HTTPException 400 if new username already taken.
    """
    user = get_user_by_id(db, user_id)

    update_fields = user_data.model_dump(exclude_unset=True)

    # If username is being changed, check uniqueness
    if "username" in update_fields:
        existing = db.query(User).filter(
            User.username == update_fields["username"],
            User.id != user_id,
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        user.username = update_fields["username"]

    # Hash password before storing
    if "password" in update_fields:
        user.password = hash_password(update_fields["password"])

    if "fullname" in update_fields:
        user.fullname = update_fields["fullname"]

    if "role" in update_fields:
        user.role = update_fields["role"]

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> dict:
    """Delete a user account.

    Raises:
        HTTPException 404 if user not found.
    """
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
    return {"detail": f"User '{user.username}' deleted successfully"}
