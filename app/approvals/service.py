from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Vacancy, ApprovalDecision, AuditEvent, VacancyStatus, DecisionEnum


def _audit(db: Session, actor_id: int, action: str, vacancy_id: int, metadata: dict = None):
    db.add(AuditEvent(
        actor_user_id=actor_id,
        action=action,
        entity_type="Vacancy",
        entity_id=vacancy_id,
        metadata_json=metadata or {},
    ))


def list_pending(db: Session) -> list[Vacancy]:
    return (
        db.query(Vacancy)
        .filter(Vacancy.status == VacancyStatus.PENDING_APPROVAL)
        .order_by(Vacancy.updated_at.asc())
        .all()
    )


def approve_vacancy(db: Session, vacancy_id: int, rh_user_id: int, justification: str | None) -> ApprovalDecision:
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    if vacancy.status != VacancyStatus.PENDING_APPROVAL:
        raise HTTPException(status_code=400, detail="Vaga não está aguardando aprovação")

    decision = ApprovalDecision(
        vacancy_id=vacancy_id,
        rh_user_id=rh_user_id,
        decision=DecisionEnum.APPROVED,
        justification=justification,
        decided_at=datetime.utcnow(),
    )
    vacancy.status = VacancyStatus.APPROVED
    vacancy.updated_at = datetime.utcnow()

    db.add(decision)
    _audit(db, rh_user_id, "VACANCY_APPROVED", vacancy_id)
    db.commit()
    db.refresh(decision)
    return decision


def reject_vacancy(db: Session, vacancy_id: int, rh_user_id: int, justification: str) -> ApprovalDecision:
    if not justification or not justification.strip():
        raise HTTPException(status_code=400, detail="Justificativa obrigatória para recusa")

    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    if vacancy.status != VacancyStatus.PENDING_APPROVAL:
        raise HTTPException(status_code=400, detail="Vaga não está aguardando aprovação")

    decision = ApprovalDecision(
        vacancy_id=vacancy_id,
        rh_user_id=rh_user_id,
        decision=DecisionEnum.REJECTED,
        justification=justification,
        decided_at=datetime.utcnow(),
    )
    vacancy.status = VacancyStatus.REJECTED
    vacancy.updated_at = datetime.utcnow()

    db.add(decision)
    _audit(db, rh_user_id, "VACANCY_REJECTED", vacancy_id, {"reason": justification})
    db.commit()
    db.refresh(decision)
    return decision
