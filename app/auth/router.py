from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.schemas import LoginRequest, TokenResponse, UserOut
from app.auth.service import create_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse, summary="Login fake (Sprint 1)")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    Login simplificado para Sprint 1.
    Informe apenas o `user_id`. Retorna um token JWT.
    - user_id=1 → REQUESTER
    - user_id=2 → RH
    """
    user = db.query(User).filter(User.id == body.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    token = create_token(user.id)
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        name=user.name,
        role=user.role,
    )


@router.get("/me", response_model=UserOut, summary="Usuário autenticado")
def me(current_user: User = Depends(get_current_user)):
    return current_user
