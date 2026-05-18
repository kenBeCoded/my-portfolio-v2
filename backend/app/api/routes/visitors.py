"""
Visitor tracking routes.

POST /api/visitors/log  — Public, rate-limited (10 req/min/IP).
GET  /api/visitors/stats — Admin-only, returns cached VisitorStatsOut.
"""

import time
import threading
from collections import defaultdict

from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.visitor import VisitorLogCreate, VisitorStatsOut
from app.services.visitor_service import log_visitor_visit, get_visitor_analytics

router = APIRouter(prefix="/visitors", tags=["Visitors"])


# ── In-memory sliding-window rate limiter (zero-dependency) ──────────────────
# Tracks per-IP request timestamps in a 60-second sliding window.
# Max 10 requests per minute per IP for the log endpoint.

_rl_lock:    threading.Lock = threading.Lock()
_rl_buckets: dict[str, list[float]] = defaultdict(list)
_RL_MAX_REQUESTS = 10
_RL_WINDOW_SECS  = 60


def _check_rate_limit(client_ip: str) -> None:
    """Raise 429 if the IP has exceeded 10 requests in the last 60 seconds."""
    now = time.monotonic()
    with _rl_lock:
        # Evict timestamps outside the sliding window
        timestamps = [t for t in _rl_buckets[client_ip] if now - t < _RL_WINDOW_SECS]
        if len(timestamps) >= _RL_MAX_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please slow down.",
            )
        timestamps.append(now)
        _rl_buckets[client_ip] = timestamps


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/log", status_code=201)
def log_visit(
    visit: VisitorLogCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Record a public portfolio visit.

    - Rate-limited: 10 requests per minute per IP.
    - Rejects paths that start with '/admin' (returns 400).
    - Returns 201 on success.
    """
    client_ip = request.client.host if request.client else "unknown"
    _check_rate_limit(client_ip)
    log_visitor_visit(db, visit)
    return {"detail": "Visit logged."}


@router.get("/stats", response_model=VisitorStatsOut)
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return aggregated visitor analytics (admin-only, 60s cached)."""
    return get_visitor_analytics(db)
