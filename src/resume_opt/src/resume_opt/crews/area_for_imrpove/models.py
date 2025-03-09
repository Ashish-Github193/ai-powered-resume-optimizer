from datetime import date
from typing import List, Optional

from pydantic import (BaseModel, EmailStr, Field, HttpUrl, field_serializer,
                      field_validator)


class ContactInfo(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    portfolio: Optional[HttpUrl] = None
    location: Optional[str] = None

    @field_serializer("linkedin", "github", "portfolio")
    def serialize_url(v):
        if v is None:
            return None
        return str(v)


class Summary(BaseModel):
    text: str


class Experience(BaseModel):
    job_title: str
    company: str
    location: Optional[str] = None
    start_date: date | str
    end_date: Optional[date | str] = Field(
        None, description="None means currently working"
    )
    description: List[str]


class Education(BaseModel):
    degree: str
    field_of_study: Optional[str] = None
    university: str
    location: Optional[str] = None
    start_date: date | str
    end_date: Optional[date | str] = Field(
        None, description="None means currently studying"
    )


class Certification(BaseModel):
    name: str
    issuing_organization: str
    issue_date: Optional[date | str] = None
    expiration_date: Optional[date | str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None

    @field_serializer("credential_url")
    def serialize_url(v):
        if v is None:
            return None
        return str(v)


class Skill(BaseModel):
    name: str
    level: Optional[str] = None  # Example: Beginner, Intermediate, Advanced


class Project(BaseModel):
    title: str
    description: str
    technologies: List[str]
    link: Optional[HttpUrl] = None

    @field_serializer("link")
    def serialize_url(v):
        if v is None:
            return None
        return str(v)


class Award(BaseModel):
    title: str
    organization: Optional[str] = None
    date_received: Optional[date] = None
    description: Optional[str] = None


class VolunteerExperience(BaseModel):
    role: str
    organization: str
    start_date: date | str
    end_date: Optional[date | str] = None
    description: Optional[str] = None


class Language(BaseModel):
    name: str
    proficiency: Optional[str] = None  # Example: Basic, Fluent, Native


class Resume(BaseModel):
    contact_info: ContactInfo | None = None
    summary: Optional[list[Summary]] = None
    experience: List[Experience] = []
    education: List[Education] = []
    certifications: List[Certification] = []
    skills: List[Skill] = []
    projects: List[Project] = []
    awards: List[Award] = []
    volunteer_experience: List[VolunteerExperience] = []
    languages: List[Language] = []


class ResumeSectionFeedback(BaseModel):
    section_name: str = Field(
        ...,
        description="Name of the resume section (e.g., 'Experience', 'Education')",
    )
    issues: List[str] = Field(
        ..., description="List of identified issues in the section"
    )
    suggested_improvements: Optional[List[str]] = Field(
        None, description="Suggested improvements for the section"
    )
    confidence_score: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        description="Confidence level of the detected issues (0 to 1)",
    )


class ResumeScore(BaseModel):
    score: float = Field(
        -1, description="Score of a section of resume between 0 and 1"
    )

    @field_validator("score")
    def check_score_range(cls, v):
        if v != -1 and (v < 0 or v > 1):
            raise ValueError("Score must be between 0 and 1 or -1 for unset")
        return v


class ResumeAnalysisResult(BaseModel):
    sections_feedback: List[str] = []  # Replace with ResumeSectionFeedback
    overall_score: Optional[ResumeScore] = ResumeScore()
    grammar_score: Optional[ResumeScore] = ResumeScore()
    formatting_score: Optional[ResumeScore] = ResumeScore()
    consistency_score: Optional[ResumeScore] = ResumeScore()
