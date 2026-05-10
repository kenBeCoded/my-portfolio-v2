"""
ProjectTechStack association table (many-to-many).

Columns: id, project_id, techstack_id
"""

from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base


class ProjectTechStack(Base):
    __tablename__ = "project_techstacks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    techstack_id = Column(Integer, ForeignKey("techstack.id", ondelete="CASCADE"), nullable=False)
