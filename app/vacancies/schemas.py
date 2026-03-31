from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models import VacancyStatus, PriorityEnum, RequirementType


# ── Requirement ───────────────────────────────────────────────────────────────

class RequirementIn(BaseModel):
    type: RequirementType
    name: str = Field(..., min_length=1, max_length=200)
    level: Optional[str] = None
    weight: float = Field(default=1.0, ge=0.0, le=10.0)
    mandatory: bool = True


class RequirementOut(RequirementIn):
    id: int
    vacancy_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Vacancy ───────────────────────────────────────────────────────────────────

class VacancyCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    location: str = Field(..., min_length=2, max_length=200)
    priority: PriorityEnum = PriorityEnum.MEDIUM
    requirements: list[RequirementIn] = []


class VacancyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    location: Optional[str] = Field(None, min_length=2, max_length=200)
    priority: Optional[PriorityEnum] = None
    requirements: Optional[list[RequirementIn]] = None


class VacancyOut(BaseModel):
    id: int
    title: str
    description: str
    location: str
    priority: PriorityEnum
    status: VacancyStatus
    requester_id: int
    created_at: datetime
    updated_at: datetime
    requirements: list[RequirementOut] = []

    model_config = {"from_attributes": True}


class VacancyList(BaseModel):
    id: int
    title: str
    location: str
    priority: PriorityEnum
    status: VacancyStatus
    requester_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
