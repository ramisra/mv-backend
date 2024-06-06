from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile, HTTPException,
)

from core.config import Settings, get_settings
from core.models.user import User
from core.services.auth import AuthService
from core.services.storage_service import StorageWrapper


router = APIRouter()


@router.post("/file/upload")
async def file_upload(
    current_user: Optional[User] = Depends(AuthService().get_current_user),
    file: UploadFile = File(
        None,
        media_type="multipart/form-data",
    ),
):
    print(file.filename)
    if not file.filename:
        raise HTTPException(status_code=404, detail="File not found")

    return StorageWrapper().upload_file(current_user, file)
