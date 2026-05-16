"""
Pydantic schemas for Project operations.
"""

from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.techstack import TechStackOut


# ── Request schemas ─────────────────────────────────────────

class ProjectCreate(BaseModel):
    """Schema for creating a new project."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    repo_url: str | None = None
    live_url: str | None = None
    project_img_url: str | None = None
    status: str = Field(default="in-progress", max_length=20)
    sort_order: int = 0
    featured: bool = False
    techstack_ids: list[int] = Field(default_factory=list, description="IDs of techstacks to assign")


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None
    repo_url: str | None = None
    live_url: str | None = None
    project_img_url: str | None = None
    status: str | None = Field(default=None, max_length=20)
    sort_order: int | None = None
    featured: bool | None = None
    techstack_ids: list[int] | None = Field(default=None, description="Replace techstack associations (None = no change)")


class ProjectTechStackUpdate(BaseModel):
    """Schema for assigning/removing techstacks from a project."""
    techstack_ids: list[int] = Field(..., description="List of techstack IDs to assign to the project")


# ── Response schemas ────────────────────────────────────────

class ProjectOut(BaseModel):
    """Schema for project responses."""
    id: int
    title: str
    description: str | None = None
    repo_url: str | None = None
    live_url: str | None = None
    project_img_url: str | None = None
    status: str
    sort_order: int
    featured: bool
    is_deleted: bool
    techstacks: list[TechStackOut] = []
    updated_at: datetime | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
