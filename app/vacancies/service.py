from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Vacancy, Requirement, AuditEvent, User, VacancyStatus, RoleEnum
from app.vacancies.schemas import VacancyCreate, VacancyUpdate


def _audit(db: Session, actor_id: int, action: str, entity_id: int, metadata: dict = None):
    event = AuditEvent(
        actor_user_id=actor_id,
        action=action,
        entity_type="Vacancy",
        entity_id=entity_id,
        metadata_json=metadata or {},
    )
    db.add(event)


def list_vacancies(db: Session, user: User) -> list[Vacancy]:
    q = db.query(Vacancy)
    if user.role == RoleEnum.REQUESTER:
        q = q.filter(Vacancy.requester_id == user.id)
    return q.order_by(Vacancy.created_at.desc()).all()


def get_vacancy_or_404(db: Session, vacancy_id: int) -> Vacancy:
    v = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return v


def create_vacancy(db: Session, data: VacancyCreate, requester_id: int) -> Vacancy:
    vacancy = Vacancy(
        title=data.title,
        description=data.description,
        location=data.location,
        priority=data.priority,
        requester_id=requester_id,
    )
    db.add(vacancy)
    db.flush()  # get ID before requirements

    for req in data.requirements:
        db.add(Requirement(vacancy_id=vacancy.id, **req.model_dump()))

    _audit(db, requester_id, "VACANCY_CREATED", vacancy.id, {"title": vacancy.title})
    db.commit()
    db.refresh(vacancy)
    return vacancy


def update_vacancy(db: Session, vacancy_id: int, data: VacancyUpdate, user: User) -> Vacancy:
    vacancy = get_vacancy_or_404(db, vacancy_id)

    if vacancy.status != VacancyStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Só vagas em DRAFT podem ser editadas")

    if vacancy.requester_id != user.id and user.role != RoleEnum.RH:
        raise HTTPException(status_code=403, detail="Sem permissão para editar esta vaga")

    for field, value in data.model_dump(exclude_none=True, exclude={"requirements"}).items():
        setattr(vacancy, field, value)

    if data.requirements is not None:
        # replace requirements
        for r in vacancy.requirements:
            db.delete(r)
        db.flush()
        for req in data.requirements:
            db.add(Requirement(vacancy_id=vacancy.id, **req.model_dump()))

    vacancy.updated_at = datetime.utcnow()
    _audit(db, user.id, "VACANCY_UPDATED", vacancy.id)
    db.commit()
    db.refresh(vacancy)
    return vacancy


def submit_vacancy(db: Session, vacancy_id: int, user: User) -> Vacancy:
    vacancy = get_vacancy_or_404(db, vacancy_id)

    if vacancy.requester_id != user.id:
        raise HTTPException(status_code=403, detail="Somente o solicitante pode submeter")

    if vacancy.status != VacancyStatus.DRAFT:
        raise HTTPException(status_code=400, detail=f"Vaga não está em DRAFT (status atual: {vacancy.status})")

    vacancy.status = VacancyStatus.PENDING_APPROVAL
    vacancy.updated_at = datetime.utcnow()
    _audit(db, user.id, "VACANCY_SUBMITTED", vacancy.id)
    db.commit()
    db.refresh(vacancy)
    return vacancy
