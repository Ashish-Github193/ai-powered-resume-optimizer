from pydantic import BaseModel


class JobPostingOptimizationRequest(BaseModel):
    resume_content: str
    job_posting: str


class ATSOptimizationRequest(BaseModel):
    resume_content: str


class AOIRequest(BaseModel):
    resume_content: str


class ScoringRequest(BaseModel):
    resume_content: str
