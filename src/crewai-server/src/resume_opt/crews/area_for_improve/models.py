from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_serializer


class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
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
    text: Optional[str] = None


class Experience(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[date | str] = Field(
        None, description="None means currently working"
    )
    description: List[str]


class Education(BaseModel):
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    university: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = Field(
        None, description="None means currently studying"
    )


class Certification(BaseModel):
    name: Optional[str] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[str] = None
    expiration_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None

    @field_serializer("credential_url")
    def serialize_url(v):
        if v is None:
            return None
        return str(v)


class Skill(BaseModel):
    name: Optional[str] = None
    level: Optional[str] = None  # Example: Beginner, Intermediate, Advanced


class Project(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str]
    link: Optional[HttpUrl] = None

    @field_serializer("link")
    def serialize_url(v):
        if v is None:
            return None
        return str(v)


class Award(BaseModel):
    title: Optional[str] = None
    organization: Optional[str] = None
    date_received: Optional[str] = None
    description: Optional[str] = None


class VolunteerExperience(BaseModel):
    role: Optional[str] = None
    organization: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None


class Language(BaseModel):
    name: Optional[str] = None
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


class ResumeAnalysisResult(BaseModel):
    sections_feedback: List[str] = []
