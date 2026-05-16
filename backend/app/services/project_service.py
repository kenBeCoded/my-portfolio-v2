"""
Project service — business logic for CRUD operations on projects.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.project import Project
from app.models.techstack import TechStack
from app.models.project_techstack import ProjectTechStack
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_all_projects(db: Session, include_archived: bool = False) -> list[Project]:
    """Return all projects.

    Args:
        include_archived: If True, return all projects including archived/deleted.
                          If False (public), exclude archived and soft-deleted.
    """
    query = db.query(Project)
    if not include_archived:
        query = query.filter(
            Project.is_deleted == False,  # noqa: E712
            Project.status != "archived",
        )
    return query.order_by(Project.sort_order).all()


def get_project_by_id(db: Session, project_id: int) -> Project:
    """Return a single project by ID.

    Raises:
        HTTPException 404 if project not found.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )
    return project


def create_project(db: Session, project_data: ProjectCreate) -> Project:
    """Create a new project and optionally assign techstacks in one transaction."""
    new_project = Project(
        title=project_data.title,
        description=project_data.description,
        repo_url=project_data.repo_url,
        live_url=project_data.live_url,
        project_img_url=project_data.project_img_url,
        status=project_data.status,
        sort_order=project_data.sort_order,
        featured=project_data.featured,
    )
    db.add(new_project)
    db.flush()  # get new_project.id without committing

    # Assign techstacks if provided
    if project_data.techstack_ids:
        valid_techstacks = (
            db.query(TechStack)
            .filter(TechStack.id.in_(project_data.techstack_ids))
            .all()
        )
        valid_ids = {ts.id for ts in valid_techstacks}
        invalid_ids = set(project_data.techstack_ids) - valid_ids
        if invalid_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid techstack IDs: {sorted(invalid_ids)}",
            )
        for ts_id in project_data.techstack_ids:
            db.add(ProjectTechStack(project_id=new_project.id, techstack_id=ts_id))

    db.commit()
    db.refresh(new_project)
    return new_project


def update_project(db: Session, project_id: int, project_data: ProjectUpdate) -> Project:
    """Update an existing project, optionally replacing its techstack associations.

    Raises:
        HTTPException 404 if project not found.
        HTTPException 400 if any supplied techstack ID is invalid.
    """
    project = get_project_by_id(db, project_id)

    update_fields = project_data.model_dump(exclude_unset=True)

    # Handle techstack replacement separately — do not setattr on the ORM model
    techstack_ids = update_fields.pop("techstack_ids", None)

    for field, value in update_fields.items():
        setattr(project, field, value)

    if techstack_ids is not None:
        # Validate supplied IDs
        valid_techstacks = (
            db.query(TechStack)
            .filter(TechStack.id.in_(techstack_ids))
            .all()
        )
        valid_ids = {ts.id for ts in valid_techstacks}
        invalid_ids = set(techstack_ids) - valid_ids
        if invalid_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid techstack IDs: {sorted(invalid_ids)}",
            )

        # Remove existing associations then re-insert
        db.query(ProjectTechStack).filter(
            ProjectTechStack.project_id == project_id
        ).delete(synchronize_session="fetch")
        for ts_id in techstack_ids:
            db.add(ProjectTechStack(project_id=project_id, techstack_id=ts_id))

    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int) -> dict:
    """Soft-delete a project by setting is_deleted to True.

    Raises:
        HTTPException 404 if project not found.
    """
    project = get_project_by_id(db, project_id)
    project.is_deleted = True
    db.commit()
    return {"detail": f"Project '{project.title}' deleted successfully"}


def update_project_techstacks(
    db: Session, project_id: int, techstack_ids: list[int]
) -> Project:
    """Replace the techstacks associated with a project.

    Raises:
        HTTPException 404 if project not found.
        HTTPException 400 if any techstack ID is invalid.
    """
    project = get_project_by_id(db, project_id)

    # Validate all techstack IDs exist
    valid_techstacks = db.query(TechStack).filter(TechStack.id.in_(techstack_ids)).all()
    valid_ids = {ts.id for ts in valid_techstacks}
    invalid_ids = set(techstack_ids) - valid_ids
    if invalid_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid techstack IDs: {sorted(invalid_ids)}",
        )

    # Remove existing associations
    db.query(ProjectTechStack).filter(
        ProjectTechStack.project_id == project_id
    ).delete(synchronize_session="fetch")

    # Create new associations
    for ts_id in techstack_ids:
        db.add(ProjectTechStack(project_id=project_id, techstack_id=ts_id))

    db.commit()
    db.refresh(project)
    return project
