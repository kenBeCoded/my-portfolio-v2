"""
Visitor service — core analytics logic with in-memory TTL caching.

All timestamp grouping uses UTC. Stats results are cached for 60 seconds
to protect the database from repeated admin dashboard refreshes.
"""

import time
import threading
from datetime import datetime, timezone, timedelta
from collections import defaultdict

from sqlalchemy import func, cast, Date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.visitor import VisitorLog
from app.schemas.visitor import (
    VisitorLogCreate,
    DailyVisitorStats,
    WeeklyVisitorStats,
    TopPageStats,
    RecentVisitorStats,
    VisitorStatsOut,
)


# ── In-memory TTL Cache (zero-dependency, thread-safe) ───────────────────────

_cache_lock   = threading.Lock()
_cache_value  = None
_cache_expiry = 0.0   # epoch seconds
CACHE_TTL_SECONDS = 60


def _get_cached_stats() -> VisitorStatsOut | None:
    with _cache_lock:
        if _cache_value is not None and time.monotonic() < _cache_expiry:
            return _cache_value
    return None


def _set_cached_stats(stats: VisitorStatsOut) -> None:
    global _cache_value, _cache_expiry
    with _cache_lock:
        _cache_value  = stats
        _cache_expiry = time.monotonic() + CACHE_TTL_SECONDS


def _invalidate_cache() -> None:
    global _cache_value, _cache_expiry
    with _cache_lock:
        _cache_value  = None
        _cache_expiry = 0.0


# ── Service functions ─────────────────────────────────────────────────────────

def log_visitor_visit(db: Session, visitor_data: VisitorLogCreate) -> VisitorLog:
    """Persist a public portfolio visit.

    Raises:
        HTTPException 400 if the path starts with '/admin' (case-insensitive).
    """
    normalized_path = visitor_data.page_path.strip().lower()
    if normalized_path.startswith("/admin") or "admin" in normalized_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tracking admin paths is not allowed.",
        )

    entry = VisitorLog(
        visitor_id=visitor_data.visitor_id,
        page_path=visitor_data.page_path,
        user_agent=visitor_data.user_agent,
        referer=visitor_data.referer,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    # Invalidate cache so the next stats fetch reflects the new visit
    _invalidate_cache()
    return entry


def get_visitor_analytics(db: Session) -> VisitorStatsOut:
    """Return aggregated visitor analytics, served from cache when available.

    Metrics:
    - Total all-time page views and unique visitors
    - Weekly unique visitors (past 7 days)
    - Daily stats: page views + unique visitors for the last 14 days (UTC)
    - Weekly stats: unique visitors grouped by UTC week for the last 8 weeks
    - Top 5 most-visited paths (all time)
    - 10 most recent visitor log entries
    """
    cached = _get_cached_stats()
    if cached is not None:
        return cached

    now_utc = datetime.now(timezone.utc)

    # ── All-time totals ───────────────────────────────────────────────────────
    total_page_views = db.query(func.count(VisitorLog.id)).scalar() or 0
    total_unique     = db.query(func.count(func.distinct(VisitorLog.visitor_id))).scalar() or 0

    # ── Weekly unique visitors (last 7 days) ──────────────────────────────────
    week_ago = now_utc - timedelta(days=7)
    weekly_unique = (
        db.query(func.count(func.distinct(VisitorLog.visitor_id)))
        .filter(VisitorLog.timestamp >= week_ago)
        .scalar()
    ) or 0

    # ── Daily stats — last 14 days ────────────────────────────────────────────
    fourteen_days_ago = now_utc - timedelta(days=14)
    daily_rows = (
        db.query(
            cast(VisitorLog.timestamp, Date).label("day"),
            func.count(VisitorLog.id).label("page_views"),
            func.count(func.distinct(VisitorLog.visitor_id)).label("unique_visitors"),
        )
        .filter(VisitorLog.timestamp >= fourteen_days_ago)
        .group_by("day")
        .order_by("day")
        .all()
    )
    daily_stats = [
        DailyVisitorStats(
            date=str(row.day),
            page_views=row.page_views,
            unique_visitors=row.unique_visitors,
        )
        for row in daily_rows
    ]

    # ── Weekly stats — last 8 weeks ───────────────────────────────────────────
    eight_weeks_ago = now_utc - timedelta(weeks=8)
    weekly_rows = (
        db.query(VisitorLog.visitor_id, VisitorLog.timestamp)
        .filter(VisitorLog.timestamp >= eight_weeks_ago)
        .all()
    )

    # Group by week (Monday as week start) in Python to stay DB-agnostic
    week_buckets: dict[str, set[str]] = defaultdict(set)
    for row in weekly_rows:
        ts = row.timestamp
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        week_start = (ts - timedelta(days=ts.weekday())).date()
        week_buckets[str(week_start)].add(row.visitor_id)

    weekly_stats = sorted(
        [
            WeeklyVisitorStats(week_start_date=wk, unique_visitors=len(visitors))
            for wk, visitors in week_buckets.items()
        ],
        key=lambda x: x.week_start_date,
    )

    # ── Top 5 pages ───────────────────────────────────────────────────────────
    top_rows = (
        db.query(
            VisitorLog.page_path,
            func.count(VisitorLog.id).label("page_views"),
        )
        .group_by(VisitorLog.page_path)
        .order_by(func.count(VisitorLog.id).desc())
        .limit(5)
        .all()
    )
    top_pages = [
        TopPageStats(page_path=row.page_path, page_views=row.page_views)
        for row in top_rows
    ]

    # ── 10 most recent visits ─────────────────────────────────────────────────
    recent_rows = (
        db.query(VisitorLog)
        .order_by(VisitorLog.timestamp.desc())
        .limit(10)
        .all()
    )
    recent_visits = [
        RecentVisitorStats(
            id=row.id,
            timestamp=row.timestamp,
            page_path=row.page_path,
            user_agent=row.user_agent,
        )
        for row in recent_rows
    ]

    # ── Assemble & cache ──────────────────────────────────────────────────────
    result = VisitorStatsOut(
        total_page_views=total_page_views,
        total_unique_visitors=total_unique,
        weekly_unique_visitors=weekly_unique,
        daily_stats=daily_stats,
        weekly_stats=weekly_stats,
        top_pages=top_pages,
        recent_visits=recent_visits,
    )
    _set_cached_stats(result)
    return result
