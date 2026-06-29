from fastapi import FastAPI

from apps.api.app.api.router import api_router
from apps.api.app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

app.include_router(
    api_router,
    prefix=settings.api_prefix,
)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {
        "message": f"{settings.app_name} is running",
        "environment": settings.environment,
    }