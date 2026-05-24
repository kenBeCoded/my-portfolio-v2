"""
FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_NAME, DEBUG, CORS_ORIGINS
from app.db.base import Base
from app.db.session import engine
import app.models  # noqa: F401 — register all models with Base.metadata
from app.api.routes.api import api_router


# ── Lifespan: create tables on startup ─────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables when the app starts."""
    Base.metadata.create_all(bind=engine)
    yield


# ── App instance ────────────────────────────────────────────
app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    debug=DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS middleware ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ───────────────────────────────────────
app.include_router(api_router, prefix="/api")


# ── Global Exception Handler ────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()  # This will print the stack trace in Render logs
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "error": str(exc),
            "type": exc.__class__.__name__,
        },
    )


# ── Health check ────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "app": APP_NAME}
