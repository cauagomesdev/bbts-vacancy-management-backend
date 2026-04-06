from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models import DecisionEnum, VacancyStatus, PriorityEnum
from app.vacancies.schemas import RequirementOut 

class ApproveRequest(BaseModel):
    justification: Optional[str] = None


class RejectRequest(BaseModel):
    justification: str  # obrigatório


class ApprovalDecisionOut(BaseModel):
    id: int
    vacancy_id: int
    rh_user_id: int
    decision: DecisionEnum
    justification: Optional[str]
    decided_at: datetime

    model_config = {"from_attributes": True}


class PendingVacancyOut(BaseModel):
    id: int
    title: str
    location: str
    priority: PriorityEnum
    status: VacancyStatus
    requester_id: int
    created_at: datetime
    requirements: list[RequirementOut] = []

    model_config = {"from_attributes": True}
