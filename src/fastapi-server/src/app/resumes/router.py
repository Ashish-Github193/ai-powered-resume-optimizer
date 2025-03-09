import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from httpx import AsyncClient, HTTPStatusError
from loguru import logger
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from app.common.utils import async_file_read, async_file_write
from app.config import (API_CONFIG_RESUME_OPTIMIZATION_URL, OUTPUT_FOLDER,
                        UPLOAD_FOLDER)
from app.resumes.models import ResumeOptimizationRequest

router = APIRouter(prefix="/resumes", tags=["Resume Optimization APIs"])


@router.post("/optimization")
async def resume_optimization(
    request: ResumeOptimizationRequest,
):
    """
    Optimize a resume based on a job posting.

    Args:
        request: ResumeOptimizationRequest containing filenames for resume and job posting

    Returns:
        Dict containing the optimization results

    Raises:
        HTTPException: If file reading or optimization fails
    """
    # File reading section with specific error handling
    try:
        resume_content_file_path = os.path.join(
            UPLOAD_FOLDER, request.resume_content_filename
        )
        if not os.path.exists(resume_content_file_path):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Resume file not found: {request.resume_content_filename}",
            )

        job_posting_file_path = os.path.join(
            UPLOAD_FOLDER, request.job_posting_filename
        )
        if not os.path.exists(job_posting_file_path):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Job posting file not found: {request.job_posting_filename}",
            )

        resume_content = await async_file_read(resume_content_file_path)
        job_posting = await async_file_read(job_posting_file_path)

    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"File not found: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error reading files: {str(e)}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading files: {str(e)}",
        )

    try:
        async with AsyncClient() as client:
            response = await client.post(
                API_CONFIG_RESUME_OPTIMIZATION_URL,
                json={
                    "resume_content": resume_content,
                    "job_posting": job_posting,
                    "choices": request.choices.model_dump(),
                },
                timeout=60.0,
            )
            response.raise_for_status()
            result = response.json()

        resume_content = result["content"]["resume"]
        resume_content_filename = (
            f"{request.resume_content_filename}_optimized.md"
        )
        resume_content_file_path = os.path.join(
            OUTPUT_FOLDER, resume_content_filename
        )
        await async_file_write(resume_content_file_path, resume_content)
        return FileResponse(
            resume_content_file_path,
            filename=resume_content_filename,
            media_type="application/octet-stream",
        )
    except HTTPStatusError as e:
        logger.error(
            f"API request failed with status {e.response.status_code}: {str(e)}"
        )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Resume optimization failed",
        )
    except TimeoutError:
        logger.error("Resume optimization request timed out")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Resume optimization request timed out",
        )
    except Exception as e:
        logger.error(f"Unexpected error during optimization: {str(e)}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during resume optimization: {str(e)}",
        )
