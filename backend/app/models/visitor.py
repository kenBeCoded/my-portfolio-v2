"""
VisitorLog SQLAlchemy model.

Columns: id, visitor_id, page_path, user_agent, referer, timestamp
Composite index on (timestamp, visitor_id) for efficient analytics grouping.
"""

from sqlalchemy import Column, Integer, String, DateTime, Index, func
from app.db.base import Base


class VisitorLog(Base):
    __tablename__ = "visitor_logs"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    visitor_id = Column(String(100), index=True, nullable=False)
    page_path  = Column(String(255), nullable=False)
    user_agent = Column(String(500), nullable=True)
    referer    = Column(String(500), nullable=True)
    timestamp  = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Composite index for fast time-series grouping queries
    __table_args__ = (
        Index("ix_visitor_logs_ts_vid", "timestamp", "visitor_id"),
    )

    def __repr__(self) -> str:
        return f"<VisitorLog id={self.id} visitor_id={self.visitor_id!r} path={self.page_path!r}>"
