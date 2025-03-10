from fastapi import APIRouter, Body, HTTPException
from loguru import logger
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from resume_engine.flows.ats_flow import ResumeOptimizationForATSFlow
from resume_engine.server.models import ATSOptimizationRequest

router = APIRouter(prefix="/ats", tags=["ATS Optimization"])


@router.post("/optimize")
async def resume_optimization(data: ATSOptimizationRequest = Body(...)):
    try:
        flow = ResumeOptimizationForATSFlow(inputs=data.model_dump())
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
