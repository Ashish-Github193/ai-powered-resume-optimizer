import os
import uuid

import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile
from starlette.status import (HTTP_400_BAD_REQUEST,
                              HTTP_500_INTERNAL_SERVER_ERROR)

from app.config import ALLOWED_EXTENSIONS_FOR_FILE_UPLOAD, UPLOAD_FOLDER

router = APIRouter(prefix="/common", tags=["Common APIs"])


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Filename is required"
        )

    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS_FOR_FILE_UPLOAD:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file_extension}. Allowed types: {', '.join(ALLOWED_EXTENSIONS_FOR_FILE_UPLOAD)}",
        )

    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    try:
        content = await file.read()
        if not content:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty",
            )

        async with aiofiles.open(file_path, "w") as out_file:
            await out_file.write(str(content))

        return {
            "message": "File uploaded successfully",
            "content": {"filename": file_name},
            "error": None,
        }

    except OSError as os_error:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File system error: {str(os_error)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while uploading the file",
        )
