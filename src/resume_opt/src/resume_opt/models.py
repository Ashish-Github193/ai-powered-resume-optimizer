from pydantic import BaseModel


class ResumeOptimizationRequest(BaseModel):
    resume_content: str
    job_posting: str


class ResumeOptimizationState(BaseModel):
    resume_contents: str = ""
    job_posting_contents: str = ""
