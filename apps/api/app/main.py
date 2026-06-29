from fastapi import FastAPI

from apps.api.app.api.router import api_router

app = FastAPI(
    title="ConvertFlow API",
    description="API para convertir y comprimir archivos.",
    version="0.1.0",
)

app.include_router(
    api_router,
    prefix="/api",
)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {
        "message": "ConvertFlow API is running",
    }