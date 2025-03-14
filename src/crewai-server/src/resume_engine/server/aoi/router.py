from fastapi import APIRouter, Body, HTTPException
from loguru import logger
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from resume_engine.flows.aoi_flow import ResumeAOIFlow
from resume_engine.server.models import AOIRequest

router = APIRouter(prefix="/aoi", tags=["Suggestion"])


@router.post("/suggest")
async def resume_optimization(data: AOIRequest = Body(...)):
    try:
        flow = ResumeAOIFlow(inputs=data.model_dump())
        await flow.kickoff_async()
        return {
            "message": "success",
            "content": {"resume": flow.state.resume_contents},
            "error": None,
        }
    except Exception as e:
        logger.error(f"Error while optimizing resume: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
