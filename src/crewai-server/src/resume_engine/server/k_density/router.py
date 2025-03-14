from fastapi import APIRouter, Body, HTTPException
from loguru import logger
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from resume_engine.flows.k_density import KeywordDensityFlow
from resume_engine.server.models import KeywordDensityOptimizationRequest

router = APIRouter(prefix="/k-density", tags=["Optimization"])


@router.post("/optimize")
async def resume_optimization(
    data: KeywordDensityOptimizationRequest = Body(...),
):
    try:
        flow = KeywordDensityFlow(inputs=data.model_dump())
        await flow.kickoff_async(inputs={"resume": data.resume_content})
        return {
            "message": "success",
            "content": {"resume": flow.state.resume_result},
            "error": None,
        }
    except Exception as e:
        logger.error(f"Error while optimizing resume: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
