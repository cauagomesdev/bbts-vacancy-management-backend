from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.service import require_rh
from app.approvals import service
from app.approvals.schemas import (
    ApproveRequest, RejectRequest, ApprovalDecisionOut, PendingVacancyOut
)

router = APIRouter(prefix="/approvals", tags=["Approvals (RH)"])


@router.get(
    "/pending",
    response_model=list[PendingVacancyOut],
    summary="Listar vagas aguardando aprovação",
)
def list_pending(
    db: Session = Depends(get_db),
    rh: User = Depends(require_rh),
):
    return service.list_pending(db)


@router.post(
    "/{vacancy_id}/approve",
    response_model=ApprovalDecisionOut,
    summary="Aprovar vaga",
)
def approve(
    vacancy_id: int,
    body: ApproveRequest,
    db: Session = Depends(get_db),
    rh: User = Depends(require_rh),
):
    return service.approve_vacancy(db, vacancy_id, rh.id, body.justification)


@router.post(
    "/{vacancy_id}/reject",
    response_model=ApprovalDecisionOut,
    summary="Recusar vaga (justificativa obrigatória)",
)
def reject(
    vacancy_id: int,
    body: RejectRequest,
    db: Session = Depends(get_db),
    rh: User = Depends(require_rh),
):
    return service.reject_vacancy(db, vacancy_id, rh.id, body.justification)
