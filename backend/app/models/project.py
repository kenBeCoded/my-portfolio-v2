"""
Project SQLAlchemy model.

Columns: id, title, description, repo_url, live_url, status,
         sort_order, featured, is_deleted, updated_at, created_at
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    repo_url = Column(String(500), nullable=True)
    live_url = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="in-progress")  # in-progress, completed, archived
    sort_order = Column(Integer, nullable=False, default=0)
    featured = Column(Boolean, nullable=False, default=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    techstacks = relationship(
        "TechStack",
        secondary="project_techstacks",
        back_populates="projects",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Project id={self.id} title={self.title!r} status={self.status!r}>"
