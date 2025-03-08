from pydantic import BaseModel


class ResumeOptimizationRequest(BaseModel):
    resume_content: str
    job_posting: str
