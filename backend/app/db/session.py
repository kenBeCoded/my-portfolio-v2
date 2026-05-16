"""
Database engine and session factory.

Configured for NeonDB (serverless PostgreSQL):
- connect_timeout=10  : fail fast instead of hanging on cold-start
- pool_pre_ping=True  : recycle stale connections after Neon suspends
- pool_recycle=300    : drop connections older than 5 min before Neon kills them
- pool_size/overflow  : stay within Neon's connection limits
- IPv4 Workaround     : resolves hostname to IPv4 to prevent 30s IPv6 hang
"""

import socket
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

# ── IPv6 Blackhole Workaround ─────────────────────────────────
# The local network/container has a broken IPv6 route. libpq 
# attempts IPv6 first and hangs for 30 seconds before falling 
# back to IPv4. We resolve the hostname to IPv4 and pass it to 
# libpq via 'hostaddr' to force an instant IPv4 connection.
parsed_url = urlparse(DATABASE_URL)
try:
    # gethostbyname only returns IPv4 addresses
    ipv4_address = socket.gethostbyname(parsed_url.hostname)
except Exception:
    ipv4_address = None

connect_args = {
    "connect_timeout": 10,   # fail fast on cold-start instead of hanging
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 5,
    "keepalives_count": 3,
}

if ipv4_address:
    connect_args["hostaddr"] = ipv4_address

engine = create_engine(
    DATABASE_URL,
    # ── NeonDB / serverless-friendly settings ───────────────────
    pool_pre_ping=True,          # test connection health before use
    pool_recycle=300,            # recycle connections every 5 min
    pool_size=5,                 # keep at most 5 persistent connections
    max_overflow=10,             # allow up to 10 extra on spike
    pool_timeout=30,             # wait max 30 s for a free connection
    # ── psycopg2 driver settings ─────────────────────────────────
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency — yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# """
# Database engine and session factory.
# """

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.core.config import DATABASE_URL

# engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
