"""
Application configuration — loads values from .env at the project root.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Database ────────────────────────────────────────────────
DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/my_portfolio")

# ── JWT / Auth ──────────────────────────────────────────────
SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "240"))  # 4 hours

# ── App ─────────────────────────────────────────────────────
APP_NAME: str = os.getenv("APP_NAME", "My Portfolio API")
DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
