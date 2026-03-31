import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.vacancies.router import router as vacancies_router
from app.approvals.router import router as approvals_router
from app.candidates.router import router as candidates_router

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("bbts")

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="BBTS — Gestão de Vagas API",
    description="""
## Sprint 1 — Backend Monólito Modular

**Fluxo principal:**
1. Solicitante cria vaga → submete para aprovação
2. RH aprova ou recusa (recusa exige justificativa)
3. Ao aprovar, candidatos sugeridos ficam disponíveis com score

**Autenticação (fake Sprint 1):**
- `POST /auth/login` com `{ "user_id": 1 }` → REQUESTER
- `POST /auth/login` com `{ "user_id": 2 }` → RH
- Use o token retornado no header `Authorization: Bearer <token>`
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global error handler ───────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error: %s", exc, exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor"})

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(vacancies_router)
app.include_router(approvals_router)
app.include_router(candidates_router)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "sprint": 1}
