"""
User SQLAlchemy model.

Columns: id, username, password, fullname, role, updated_at, created_at
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # stores bcrypt hash
    fullname = Column(String(150), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} role={self.role!r}>"
