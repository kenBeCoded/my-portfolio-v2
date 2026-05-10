"""
Project routes — public and private endpoints for project management.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut, ProjectTechStackUpdate
from app.services.project_service import (
    get_all_projects,
    create_project,
    update_project,
    delete_project,
    update_project_techstacks,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=list[ProjectOut])
def list_projects(
    include_all: bool = Query(False, description="If true, include archived/deleted (requires auth)"),
    db: Session = Depends(get_db),
):
    """List all projects.

    Public: only non-archived, non-deleted projects.
    Pass include_all=true to include all (for admin use).
    """
    return get_all_projects(db, include_archived=include_all)


@router.post("/", response_model=ProjectOut, status_code=201)
def create_new_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new project (protected route)."""
    return create_project(db, project_data)


@router.put("/{project_id}", response_model=ProjectOut)
def update_existing_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing project (protected route)."""
    return update_project(db, project_id, project_data)


@router.delete("/{project_id}")
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft-delete a project (protected route)."""
    return delete_project(db, project_id)


@router.patch("/{project_id}/techstacks", response_model=ProjectOut)
def assign_techstacks(
    project_id: int,
    data: ProjectTechStackUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Assign/replace techstacks for a project (protected route)."""
    return update_project_techstacks(db, project_id, data.techstack_ids)
