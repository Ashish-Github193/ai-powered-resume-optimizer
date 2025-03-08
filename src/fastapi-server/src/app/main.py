import os
from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError

from app.common.router import router as common_router
from app.config import APP_CONFIGS, OUTPUT_FOLDER, SHARED_FOLDER, UPLOAD_FOLDER
from app.resumes.router import router as resumes_router


@asynccontextmanager
async def lifespan(app):
    os.makedirs(SHARED_FOLDER, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    yield


app = FastAPI(
    debug=APP_CONFIGS["debug"],
    title="FastAPI",
    description="Authentication API",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    root_path="/api",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=APP_CONFIGS["allow_origins"],
    allow_credentials=APP_CONFIGS["allow_credentials"],
    allow_methods=APP_CONFIGS["allow_methods"],
    allow_headers=APP_CONFIGS["allow_headers"],
)

# Include routers
app.include_router(common_router)
app.include_router(resumes_router)


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
