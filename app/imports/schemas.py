from typing import Optional
from pydantic import BaseModel

class SkillIn(BaseModel):
    name: str
    level: Optional[str] = None
    years_experience: Optional[float] = None

class ExperienceIn(BaseModel):
    company: str
    role: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    current: bool = False

class EducationIn(BaseModel):
    institution: str
    course: str
    degree: Optional[str] = None
    graduation_year: Optional[int] = None

class LanguageIn(BaseModel):
    name: str
    level: Optional[str] = None

class CertificationIn(BaseModel):
    name: str
    issuer: Optional[str] = None
    year: Optional[int] = None

class CandidateIn(BaseModel):
    full_name: str
    headline: str = ""
    email: Optional[str] = None
    location: str = ""
    linkedin_url: Optional[str] = None
    skills: list[SkillIn] = []
    experiences: list[ExperienceIn] = []
    educations: list[EducationIn] = []
    languages: list[LanguageIn] = []
    certifications: list[CertificationIn] = []

class IntegrationLogOut(BaseModel):
    id: int
    source: str
    filename: Optional[str]
    status: str
    total_records: int
    success_count: int
    error_count: int
    errors_json: Optional[list] = None
    model_config = {"from_attributes": True}
