from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.service import get_current_user
from app.candidates import service
from app.candidates.schemas import CandidateOut

router = APIRouter(prefix="/vacancies", tags=["Candidates"])


@router.get(
    "/{vacancy_id}/candidates",
    response_model=list[CandidateOut],
    summary="Candidatos sugeridos para a vaga (ordenado por score desc)",
)
def get_candidates(
    vacancy_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Retorna candidatos mockados ordenados por score (0-100).
    Cada candidato inclui `explanation` com requisitos atendidos,
    obrigatórios faltantes e pontos fortes.
    """
    return service.get_candidates(db, vacancy_id)
