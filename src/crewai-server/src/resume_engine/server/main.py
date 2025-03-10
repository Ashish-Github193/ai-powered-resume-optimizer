from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError

from resume_engine.server.aoi.router import router as aoi_router

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
