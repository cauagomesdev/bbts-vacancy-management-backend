from pydantic import BaseModel


class CandidateExplanation(BaseModel):
    met_requirements: int
    total_requirements: int
    missing_mandatory: list[str]
    strengths: list[str]


class CandidateOut(BaseModel):
    id: int
    vacancy_id: int
    full_name: str
    headline: str
    location: str
    score: float
    explanation: CandidateExplanation

    model_config = {"from_attributes": True}
