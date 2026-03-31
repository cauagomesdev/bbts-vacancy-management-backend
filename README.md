# BBTS — Gestão de Vagas · Backend Sprint 1

API REST para gestão de vagas, aprovação RH e ranking de candidatos.  
Stack: **FastAPI · PostgreSQL · SQLAlchemy · Alembic · Docker**

---

## Pré-requisitos

- Docker + Docker Compose
- **OU** Python 3.11+ e PostgreSQL local

---

## Subir com Docker (recomendado)

```bash
# 1. Clone e entre na pasta
git clone https://github.com/FMello-Dev/bbts-vacancy-management-frontend.git
cd bbts-backend

# 2. Suba tudo (Postgres + API + migrations + seed automáticos)
docker compose up --build
```

A API estará em **http://localhost:8000**  
Swagger UI: **http://localhost:8000/docs**  
ReDoc:      **http://localhost:8000/redoc**

---

## Rodar localmente (sem Docker)

```bash
# 1. Ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Copiar e ajustar variáveis de ambiente
cp .env.example .env
# Edite DATABASE_URL para apontar para seu Postgres local

# 4. Rodar migrations
alembic upgrade head

# 5. Popular banco com dados de demo
python seed.py

# 6. Iniciar API
uvicorn app.main:app --reload --port 8000
```

---

## Estrutura de pastas

```
bbts-backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, routers
│   ├── config.py            # Settings (pydantic-settings)
│   ├── database.py          # Engine, SessionLocal, Base
│   ├── models.py            # Todos os modelos SQLAlchemy
│   ├── auth/
│   │   ├── router.py        # POST /auth/login · GET /auth/me
│   │   ├── service.py       # JWT · guards (get_current_user, require_rh)
│   │   └── schemas.py
│   ├── vacancies/
│   │   ├── router.py        # CRUD vagas + submit
│   │   ├── service.py
│   │   └── schemas.py
│   ├── approvals/
│   │   ├── router.py        # GET pending · POST approve/reject
│   │   ├── service.py
│   │   └── schemas.py
│   ├── candidates/
│   │   ├── router.py        # GET /vacancies/:id/candidates
│   │   ├── service.py
│   │   └── schemas.py
│   └── connectors/
│       └── base.py          # ProfileConnector (interface Sprint 2+)
├── alembic/
│   ├── env.py
│   └── versions/001_initial.py
├── seed.py
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── alembic.ini
└── requirements.txt
```

---

## Fluxo de demo passo a passo

### 1. Obter token de REQUESTER

```http
POST /auth/login
{ "user_id": 1 }
```
→ Copie o `access_token` retornado.

### 2. Criar uma vaga

```http
POST /vacancies
Authorization: Bearer <token_requester>

{
  "title": "Analista de QA Sênior",
  "description": "Responsável pela estratégia de testes do squad de pagamentos.",
  "location": "São Paulo, SP",
  "priority": "HIGH",
  "requirements": [
    { "type": "SKILL", "name": "Selenium", "level": "Avançado", "weight": 3.0, "mandatory": true },
    { "type": "SKILL", "name": "Cypress", "weight": 2.0, "mandatory": false },
    { "type": "LANGUAGE", "name": "Inglês", "level": "Intermediário", "weight": 1.0, "mandatory": false }
  ]
}
```

### 3. Submeter para aprovação

```http
POST /vacancies/{id}/submit
Authorization: Bearer <token_requester>
```

### 4. Obter token de RH

```http
POST /auth/login
{ "user_id": 2 }
```

### 5. Ver vagas pendentes

```http
GET /approvals/pending
Authorization: Bearer <token_rh>
```

### 6a. Aprovar

```http
POST /approvals/{vacancyId}/approve
Authorization: Bearer <token_rh>

{ "justification": "Perfil estratégico para Q3." }
```

### 6b. Ou recusar (justificativa obrigatória)

```http
POST /approvals/{vacancyId}/reject
Authorization: Bearer <token_rh>

{ "justification": "Budget não aprovado para este trimestre." }
```

### 7. Ver candidatos sugeridos (vaga seed com id=3)

```http
GET /vacancies/3/candidates
Authorization: Bearer <token_rh>
```

---

## Usuários do seed

| id | Nome       | Email             | Role      |
|----|------------|-------------------|-----------|
| 1  | Ana Souza  | ana@bbts.com      | REQUESTER |
| 2  | Carlos RH  | carlos@bbts.com   | RH        |

## Vagas do seed

| id | Título                              | Status             |
|----|-------------------------------------|--------------------|
| 1  | Desenvolvedor Frontend Sênior       | DRAFT              |
| 2  | Engenheiro de Dados Pleno           | PENDING_APPROVAL   |
| 3  | Tech Lead Backend (Java / Spring)   | APPROVED + candidatos |

---

## RBAC resumido

| Endpoint                          | REQUESTER | RH  |
|-----------------------------------|:---------:|:---:|
| POST /auth/login                  | ✅        | ✅  |
| GET /vacancies                    | ✅ (só suas) | ✅ |
| POST /vacancies                   | ✅        | ✅  |
| PATCH /vacancies/:id              | ✅ (se dono) | ✅ |
| POST /vacancies/:id/submit        | ✅ (se dono) | ❌ |
| GET /approvals/pending            | ❌        | ✅  |
| POST /approvals/:id/approve       | ❌        | ✅  |
| POST /approvals/:id/reject        | ❌        | ✅  |
| GET /vacancies/:id/candidates     | ✅        | ✅  |

---

## Próximas sprints

- [ ] Implementar `GupyConnector`, `GoogleTalentConnector`, `EmpregaNetConnector`  
      (contrato já definido em `app/connectors/base.py`)
- [ ] Motor de scoring real (pesos × requisitos atendidos)
- [ ] SSO / autenticação real
- [ ] Notificações por e-mail ao aprovar/recusar
