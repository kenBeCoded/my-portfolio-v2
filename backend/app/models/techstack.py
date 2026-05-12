"""
TechStack SQLAlchemy model.

Columns: id, name, category, sort_order, updated_at, created_at
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class TechStack(Base):
    __tablename__ = "techstack"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=False)  # e.g. language, framework, database, devops
    logo_url = Column(String(255), nullable=True)  # URL to the technology logo
    sort_order = Column(Integer, nullable=False, default=0)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    projects = relationship(
        "Project",
        secondary="project_techstacks",
        back_populates="techstacks",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<TechStack id={self.id} name={self.name!r} category={self.category!r}>"
