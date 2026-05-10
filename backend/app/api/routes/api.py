"""
Unified API router — aggregates all route modules under a single router.
"""

from fastapi import APIRouter

from app.api.routes import auth, users, projects, techstacks

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(projects.router)
api_router.include_router(techstacks.router)
