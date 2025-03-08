from fastapi import Body, FastAPI, HTTPException
from loguru import logger
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from resume_opt.flow import ResumeOptimizationFlow
from resume_opt.models import ResumeOptimizationRequest

app = FastAPI(
    title="Resume Optimization API",
    description="Optimize resume for job posting and ATS compliance",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    root_path="/api",
)


@app.post("/api/resumes/optimization")
async def resume_optimization(data: ResumeOptimizationRequest = Body(...)):
    try:
        flow = ResumeOptimizationFlow(inputs=data.model_dump())
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
