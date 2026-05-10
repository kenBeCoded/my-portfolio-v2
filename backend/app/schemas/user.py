"""
Pydantic schemas for User operations.
"""

from datetime import datetime
from pydantic import BaseModel, Field


# ── Request schemas ─────────────────────────────────────────

class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    fullname: str = Field(..., min_length=1, max_length=150)
    role: str = Field(default="user", max_length=20)


class UserUpdate(BaseModel):
    """Schema for updating user profile (username or password)."""
    username: str | None = Field(default=None, min_length=3, max_length=50)
    password: str | None = Field(default=None, min_length=6)
    fullname: str | None = Field(default=None, max_length=150)
    role: str | None = Field(default=None, max_length=20)


# ── Response schemas ────────────────────────────────────────

class UserOut(BaseModel):
    """Schema for user responses (never exposes password)."""
    id: int
    username: str
    fullname: str
    role: str
    updated_at: datetime | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
