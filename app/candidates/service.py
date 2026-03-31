from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import CandidateSuggestion, Vacancy
from app.candidates.schemas import CandidateOut, CandidateExplanation


def get_candidates(db: Session, vacancy_id: int) -> list[CandidateOut]:
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")

    suggestions = (
        db.query(CandidateSuggestion)
        .filter(CandidateSuggestion.vacancy_id == vacancy_id)
        .order_by(CandidateSuggestion.score.desc())
        .all()
    )

    result = []
    for s in suggestions:
        exp = s.explanation_json
        result.append(CandidateOut(
            id=s.id,
            vacancy_id=s.vacancy_id,
            full_name=s.full_name,
            headline=s.headline,
            location=s.location,
            score=s.score,
            explanation=CandidateExplanation(**exp),
        ))
    return result
