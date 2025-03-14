from typing import Optional

from pydantic import BaseModel


class ResumeBreakdownResult(BaseModel):
    header_and_summary: Optional[str] = None
    skills_section: Optional[str] = None
    work_experience: Optional[str] = None
    education_and_certifications: Optional[str] = None
    additional_sections: Optional[str] = None
