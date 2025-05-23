from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError

from resume_engine.server.aoi.router import router as aoi_router
from resume_engine.server.ats.router import router as ats_router
from resume_engine.server.job_posting.router import \
    router as job_posting_router
from resume_engine.server.k_density.router import router as k_density_router
from resume_engine.server.scoring.router import router as scoring_router

app = FastAPI(
    title="Resume Optimization API",
    description="Optimize resume for job posting and ATS compliance",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    root_path="/api",
)

# Register the routers
app.include_router(aoi_router)
app.include_router(ats_router)
app.include_router(job_posting_router)
app.include_router(scoring_router)
app.include_router(k_density_router)


# Define exception handlers
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    detail = exc.errors()[0]["msg"] if exc.errors() else "Validation Error"
    logger.error(f"Validation error: {exc.errors()}")
    raise HTTPException(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail
    )


@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    detail = exc.errors()[0]["msg"] if exc.errors() else "Validation Error"
    logger.error(f"Validation error: {exc.errors()}")
    raise HTTPException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=detail
    )
