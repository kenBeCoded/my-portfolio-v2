"""
TechStack service — business logic for CRUD operations on techstacks.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.techstack import TechStack
from app.schemas.techstack import TechStackCreate, TechStackUpdate


def get_all_techstacks(db: Session) -> list[TechStack]:
    """Return all techstacks ordered by sort_order."""
    return db.query(TechStack).order_by(TechStack.sort_order).all()


def get_techstack_by_id(db: Session, techstack_id: int) -> TechStack:
    """Return a single techstack by ID.

    Raises:
        HTTPException 404 if techstack not found.
    """
    techstack = db.query(TechStack).filter(TechStack.id == techstack_id).first()
    if not techstack:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TechStack with id {techstack_id} not found",
        )
    return techstack


def create_techstack(db: Session, techstack_data: TechStackCreate) -> TechStack:
    """Create a new techstack entry.

    Raises:
        HTTPException 400 if name already exists.
    """
    existing = db.query(TechStack).filter(TechStack.name == techstack_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"TechStack '{techstack_data.name}' already exists",
        )

    new_techstack = TechStack(
        name=techstack_data.name,
        category=techstack_data.category,
        sort_order=techstack_data.sort_order,
    )
    db.add(new_techstack)
    db.commit()
    db.refresh(new_techstack)
    return new_techstack


def update_techstack(
    db: Session, techstack_id: int, techstack_data: TechStackUpdate
) -> TechStack:
    """Update an existing techstack.

    Raises:
        HTTPException 404 if techstack not found.
        HTTPException 400 if new name already taken.
    """
    techstack = get_techstack_by_id(db, techstack_id)

    update_fields = techstack_data.model_dump(exclude_unset=True)

    # If name is being changed, check uniqueness
    if "name" in update_fields:
        existing = db.query(TechStack).filter(
            TechStack.name == update_fields["name"],
            TechStack.id != techstack_id,
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"TechStack '{update_fields['name']}' already exists",
            )

    for field, value in update_fields.items():
        setattr(techstack, field, value)

    db.commit()
    db.refresh(techstack)
    return techstack


def delete_techstack(db: Session, techstack_id: int) -> dict:
    """Delete a techstack entry.

    Raises:
        HTTPException 404 if techstack not found.
    """
    techstack = get_techstack_by_id(db, techstack_id)
    db.delete(techstack)
    db.commit()
    return {"detail": f"TechStack '{techstack.name}' deleted successfully"}
