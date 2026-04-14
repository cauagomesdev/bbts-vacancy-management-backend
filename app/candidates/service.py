from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models import CandidateSuggestion, Candidate, Vacancy
from app.candidates.schemas import CandidateOut, CandidateExplanation, CandidateDetailOut

def get_candidates(db: Session, vacancy_id: int) -> list[CandidateOut]:
    if not db.query(Vacancy).filter(Vacancy.id == vacancy_id).first():
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    suggestions = db.query(CandidateSuggestion).options(joinedload(CandidateSuggestion.candidate)).filter(CandidateSuggestion.vacancy_id == vacancy_id).order_by(CandidateSuggestion.score.desc()).all()
    return [CandidateOut(id=s.id, vacancy_id=s.vacancy_id, candidate_id=s.candidate_id, full_name=s.candidate.full_name, headline=s.candidate.headline, location=s.candidate.location, score=s.score, explanation=CandidateExplanation(**s.explanation_json)) for s in suggestions]

def get_candidate_detail(db: Session, candidate_id: int) -> CandidateDetailOut:
    c = db.query(Candidate).options(joinedload(Candidate.skills), joinedload(Candidate.experiences), joinedload(Candidate.educations), joinedload(Candidate.languages), joinedload(Candidate.certifications)).filter(Candidate.id == candidate_id).first()
    if not c: raise HTTPException(status_code=404, detail="Candidato não encontrado")
    return CandidateDetailOut.model_validate(c)
