from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from apps.api.app.core.config import settings

router = APIRouter(
    prefix="/files",
    tags=["Files"],
)

ALLOWED_EXTENSIONS = {
    ".csv",
    ".json",
    ".txt",
    ".xlsx",
    ".docx",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
}


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    file: UploadFile = File(...),
) -> dict[str, str | int]:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file must have a filename.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file extension: {extension or 'none'}",
        )

    content = await file.read()

    max_size_bytes = settings.max_file_size_mb * 1024 * 1024

    if len(content) > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=(
                f"File exceeds the maximum size of "
                f"{settings.max_file_size_mb} MB."
            ),
        )

    upload_directory = settings.storage_path / "uploads"
    upload_directory.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid4()}{extension}"
    destination = upload_directory / stored_name

    destination.write_bytes(content)

    return {
        "original_name": file.filename,
        "stored_name": stored_name,
        "content_type": file.content_type or "application/octet-stream",
        "size_bytes": len(content),
        "extension": extension,
    }