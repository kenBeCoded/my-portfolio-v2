"""
Pydantic schemas for TechStack operations.
"""

from datetime import datetime
from pydantic import BaseModel, Field


# ── Request schemas ─────────────────────────────────────────

class TechStackCreate(BaseModel):
    """Schema for creating a new techstack entry."""
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    logo_url: str | None = Field(default=None, max_length=255)
    sort_order: int = 0


class TechStackUpdate(BaseModel):
    """Schema for updating a techstack entry."""
    name: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=50)
    logo_url: str | None = Field(default=None, max_length=255)
    sort_order: int | None = None


# ── Response schemas ────────────────────────────────────────

class TechStackOut(BaseModel):
    """Schema for techstack responses."""
    id: int
    name: str
    category: str
    logo_url: str | None = None
    sort_order: int
    updated_at: datetime | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
