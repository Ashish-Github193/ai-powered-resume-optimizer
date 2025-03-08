import os
from typing import ClassVar

from pydantic import BaseModel, field_validator

from app.common.utils import file_exists_in_uploads_folder
from app.config import ALLOWED_EXTENSIONS_FOR_RESUMES


class ResumeOptimizationRequest(BaseModel):
    resume_content_filename: str
    job_posting_filename: str

    # Define this as a class variable since it's constant
    ALLOWED_EXTENSIONS: ClassVar[set] = set(ALLOWED_EXTENSIONS_FOR_RESUMES)

    @field_validator("resume_content_filename", "job_posting_filename")
    def validate_file_extension(cls, v, field):
        if not v.endswith(tuple(cls.ALLOWED_EXTENSIONS)):
            raise ValueError(
                f"Invalid file extension for {field.name}: {v}. "
                f"Allowed extensions are: {', '.join(cls.ALLOWED_EXTENSIONS)}"
            )
        return v

    @field_validator("resume_content_filename", "job_posting_filename")
    def validate_file_exists(cls, v, field):
        if not file_exists_in_uploads_folder(v):
            raise ValueError(
                f"{field.name.replace('_', ' ').title()} does not exist: {v}"
            )
        return v
