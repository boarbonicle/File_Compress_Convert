from fastapi import APIRouter

from apps.api.app.api.routes.files import router as files_router
from apps.api.app.api.routes.health import router as health_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(files_router)