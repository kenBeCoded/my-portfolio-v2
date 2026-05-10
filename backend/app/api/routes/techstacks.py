"""
TechStack routes — public listing and protected CRUD endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.techstack import TechStackCreate, TechStackUpdate, TechStackOut
from app.services.techstack_service import (
    get_all_techstacks,
    create_techstack,
    update_techstack,
    delete_techstack,
)

router = APIRouter(prefix="/techstacks", tags=["TechStacks"])


@router.get("/", response_model=list[TechStackOut])
def list_techstacks(db: Session = Depends(get_db)):
    """List all techstacks (public route)."""
    return get_all_techstacks(db)


@router.post("/", response_model=TechStackOut, status_code=201)
def create_new_techstack(
    techstack_data: TechStackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new techstack entry (protected route)."""
    return create_techstack(db, techstack_data)


@router.put("/{techstack_id}", response_model=TechStackOut)
def update_existing_techstack(
    techstack_id: int,
    techstack_data: TechStackUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a techstack entry (protected route)."""
    return update_techstack(db, techstack_id, techstack_data)


@router.delete("/{techstack_id}")
def delete_existing_techstack(
    techstack_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a techstack entry (protected route)."""
    return delete_techstack(db, techstack_id)
