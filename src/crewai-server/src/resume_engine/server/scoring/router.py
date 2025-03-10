from fastapi import APIRouter, Body, HTTPException
from loguru import logger
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from resume_engine.flows.scoring_flow import ResumeScoringFlow
from resume_engine.server.models import ScoringRequest

router = APIRouter(prefix="/scoring", tags=["Scoring"])


@router.post("/calculate")
async def resume_optimization(data: ScoringRequest = Body(...)):
    try:
        flow = ResumeScoringFlow(inputs=data.model_dump())
        await flow.kickoff_async()
        return {
            "message": "success",
            "content": {
                "grammar": flow.state.grammar_score,
                "consistency": flow.state.consistency_score,
                "formatting": flow.state.formatting_score,
                "overall": flow.state.overall_score,
            },
            "error": None,
        }
    except Exception as e:
        logger.error(f"Error while optimizing resume: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
