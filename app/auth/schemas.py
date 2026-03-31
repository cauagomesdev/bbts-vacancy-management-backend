"""
auth/schemas.py  ·  auth/service.py  ·  auth/router.py  (single file for brevity)
"""
# ── schemas ───────────────────────────────────────────────────────────────────
from pydantic import BaseModel
from app.models import RoleEnum


class LoginRequest(BaseModel):
    user_id: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    name: str
    role: RoleEnum


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum

    model_config = {"from_attributes": True}
