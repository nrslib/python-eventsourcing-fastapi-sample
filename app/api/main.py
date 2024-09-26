from fastapi import APIRouter

from app.api.endpoints import docs

api_router = APIRouter()
api_router.include_router(docs.router, prefix="/api", tags=["docs"])
