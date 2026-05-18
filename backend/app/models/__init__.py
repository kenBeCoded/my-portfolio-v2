# Import all models so SQLAlchemy registers them with Base.metadata
from app.models.user import User  # noqa: F401
from app.models.project import Project  # noqa: F401
from app.models.techstack import TechStack  # noqa: F401
from app.models.project_techstack import ProjectTechStack  # noqa: F401
from app.models.visitor import VisitorLog  # noqa: F401
