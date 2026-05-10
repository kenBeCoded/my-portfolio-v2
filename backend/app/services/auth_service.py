"""
Authentication service — business logic for register, login, and user lookup.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.hash import hash_password, verify_password
from app.core.security import create_access_token


def register_user(db: Session, user_data: UserCreate) -> User:
    """Register a new user.

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


def authenticate_user(db: Session, username: str, password: str) -> dict:
    """Validate credentials and return a JWT token dict.

    Raises:
        HTTPException 401 on invalid credentials.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_user_by_username(db: Session, username: str) -> User | None:
    """Look up a user by username."""
    return db.query(User).filter(User.username == username).first()
