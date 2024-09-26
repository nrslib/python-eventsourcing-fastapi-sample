from fastapi import APIRouter

from app.api.endpoints import documents
from app.api.endpoints import effective

api_router = APIRouter()

api_router.include_router(documents.router, prefix="/api", tags=["docs"])
api_router.include_router(effective.router, prefix="/api", tags=["effective"])
