from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.service import get_current_user
from app.candidates import service
from app.candidates.schemas import CandidateOut, CandidateDetailOut

router = APIRouter(tags=["Candidates"])

@router.get("/vacancies/{vacancy_id}/candidates", response_model=list[CandidateOut], summary="Candidatos por vaga (score desc)")
def get_candidates(vacancy_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return service.get_candidates(db, vacancy_id)

@router.get("/candidates/{candidate_id}", response_model=CandidateDetailOut, summary="Perfil completo do candidato")
def get_candidate_detail(candidate_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return service.get_candidate_detail(db, candidate_id)
