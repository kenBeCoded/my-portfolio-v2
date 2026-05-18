"""
Pydantic schemas for Visitor tracking operations.
"""

import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


# ── Request schemas ──────────────────────────────────────────

class VisitorLogCreate(BaseModel):
    """Schema for an incoming visit event from the public portfolio."""
    visitor_id: str = Field(..., min_length=8, max_length=100)
    page_path:  str = Field(..., max_length=255)
    user_agent: str | None = Field(default=None, max_length=500)
    referer:    str | None = Field(default=None, max_length=500)

    @field_validator("visitor_id")
    @classmethod
    def validate_visitor_id(cls, v: str) -> str:
        """Enforce safe alphanumeric format to prevent injection attacks."""
        if not re.match(r"^[a-zA-Z0-9_-]{8,100}$", v):
            raise ValueError(
                "visitor_id must be 8–100 characters: letters, digits, _ or - only."
            )
        return v


# ── Response sub-schemas ─────────────────────────────────────

class DailyVisitorStats(BaseModel):
    """Aggregated visitor stats for a single UTC day."""
    date:            str
    page_views:      int
    unique_visitors: int


class WeeklyVisitorStats(BaseModel):
    """Aggregated unique visitors for a single UTC week."""
    week_start_date: str
    unique_visitors: int


class TopPageStats(BaseModel):
    """A page path and its total hit count."""
    page_path:  str
    page_views: int


class RecentVisitorStats(BaseModel):
    """A single recent visitor log entry."""
    id:         int
    timestamp:  datetime
    page_path:  str
    user_agent: str | None = None

    model_config = {"from_attributes": True}


# ── Unified response schema ──────────────────────────────────

class VisitorStatsOut(BaseModel):
    """Unified analytics response served to the admin dashboard."""
    total_page_views:      int
    total_unique_visitors: int
    weekly_unique_visitors: int

    daily_stats:   list[DailyVisitorStats]
    weekly_stats:  list[WeeklyVisitorStats]
    top_pages:     list[TopPageStats]
    recent_visits: list[RecentVisitorStats]
