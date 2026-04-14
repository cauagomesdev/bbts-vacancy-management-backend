# BBTS — Gestão de Vagas · Backend

API REST para gestão de vagas, aprovação RH, ranking de candidatos e importação de perfis.  
Stack: **FastAPI · PostgreSQL · SQLAlchemy · Alembic · Docker**

---

## Pré-requisitos

- Docker + Docker Compose
- **OU** Python 3.11+ e PostgreSQL local

---

## Subir com Docker (recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/cauagomesdev/bbts-vacancy-management-backend.git
cd bbts-vacancy-management-backend

# 2. Suba tudo
docker compose up --build
```

A API estará em **http://localhost:8000**  
Swagger UI: **http://localhost:8000/docs**  
ReDoc: **http://localhost:8000/redoc**

---

## Rodar localmente (sem Docker)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # ajuste DATABASE_URL se necessário
alembic upgrade head
python seed.py
uvicorn app.main:app --reload --port 8000
```

---

## Migrations e Seed

```bash
# Aplicar todas as migrations
docker compose exec api alembic upgrade head

# Popular banco com dados de demonstração (executar uma vez)
docker compose exec api python seed.py

# Resetar dados de demo a qualquer momento
docker compose exec api python seed.py
```

---

## Estrutura de pastas

```
app/
├── main.py              # FastAPI app, CORS, routers
├── config.py            # Settings via .env
├── database.py          # Engine + SessionLocal
├── models.py            # Todos os modelos SQLAlchemy
├── auth/                # Login fake JWT · guards
├── vacancies/           # CRUD vagas + submit
├── approvals/           # Approve/Reject (RH only) + dispara scoring
├── candidates/          # Ranking por vaga + detalhe do candidato
├── imports/             # Import CSV e JSON + IntegrationLog
├── scoring/             # Motor de score (peso + penalidade obrigatórios)
└── connectors/          # ProfileConnector — interface para Sprint 3+
alembic/
├── env.py
└── versions/
    ├── 001_initial.py   # Sprint 1: users, vacancies, requirements, approvals, audit
    └── 002_sprint2.py   # Sprint 2: candidates (rico), integration_logs
seed.py
docker-compose.yml
Dockerfile
```

---

## Endpoints

### Auth
| Método | Rota | Descrição | Role |
|--------|------|-----------|------|
| POST | `/auth/login` | Login com `{ "user_id": 1 }` | Todos |
| GET | `/auth/me` | Usuário autenticado | Todos |

### Vagas
| Método | Rota | Descrição | Role |
|--------|------|-----------|------|
| GET | `/vacancies` | Listar vagas | REQUESTER (só suas) / RH (todas) |
| POST | `/vacancies` | Criar vaga + requisitos | Todos |
| GET | `/vacancies/:id` | Detalhe da vaga | Todos |
| PATCH | `/vacancies/:id` | Editar vaga (apenas DRAFT) | Todos |
| POST | `/vacancies/:id/submit` | Submeter para aprovação | REQUESTER |

### Aprovações
| Método | Rota | Descrição | Role |
|--------|------|-----------|------|
| GET | `/approvals/pending` | Vagas aguardando aprovação | RH |
| POST | `/approvals/:id/approve` | Aprovar + calcular scores | RH |
| POST | `/approvals/:id/reject` | Recusar (justificativa obrigatória) | RH |

### Candidatos
| Método | Rota | Descrição | Role |
|--------|------|-----------|------|
| GET | `/vacancies/:id/candidates` | Ranking de candidatos por score | Todos |
| GET | `/candidates/:id` | Perfil completo do candidato | Todos |

### Import
| Método | Rota | Descrição | Role |
|--------|------|-----------|------|
| POST | `/candidates/import/json` | Importar candidatos via JSON | RH |
| POST | `/candidates/import/csv` | Importar candidatos via CSV | RH |
| GET | `/candidates/import/template` | Baixar template CSV | RH |

---

## Fluxo de demo

### 1. Login como REQUESTER
```http
POST /auth/login
{ "user_id": 1 }
```

### 2. Criar vaga
```http
POST /vacancies
Authorization: Bearer <token>

{
  "title": "Analista de QA Sênior",
  "description": "Responsável pela estratégia de testes.",
  "location": "São Paulo, SP",
  "priority": "HIGH",
  "requirements": [
    { "type": "SKILL", "name": "Selenium", "weight": 3.0, "mandatory": true },
    { "type": "LANGUAGE", "name": "Inglês", "weight": 1.0, "mandatory": false }
  ]
}
```

### 3. Submeter para aprovação
```http
POST /vacancies/{id}/submit
Authorization: Bearer <token_requester>
```

### 4. Login como RH e aprovar
```http
POST /auth/login
{ "user_id": 2 }

POST /approvals/{id}/approve
Authorization: Bearer <token_rh>
{ "justification": "Perfil estratégico." }
```

> Ao aprovar, o sistema calcula automaticamente o score de **todos os candidatos** da base contra os requisitos da vaga e salva no banco.

### 5. Ver candidatos rankeados
```http
GET /vacancies/{id}/candidates
Authorization: Bearer <token>
```

### 6. Importar candidatos (RH)
```http
POST /candidates/import/json
Authorization: Bearer <token_rh>

[
  {
    "full_name": "João Silva",
    "email": "joao@email.com",
    "location": "São Paulo, SP",
    "skills": [{ "name": "Python", "level": "Avançado", "years_experience": 5 }],
    "languages": [{ "name": "Inglês", "level": "B2" }],
    "certifications": [],
    "educations": [],
    "experiences": []
  }
]
```

---

## Formato CSV para importação

```
full_name,headline,email,location,linkedin_url,skills,languages,certifications,education,experiences
João Silva,Dev Backend,joao@email.com,São Paulo SP,,Python:Avançado:5;FastAPI:Inter:2,Inglês:B2,AWS:Amazon:2023,USP:CC:Bach:2018,BBTS:Dev:2022:2024:false
```

Campos compostos: `;` separa itens, `:` separa sub-campos.

---

## Usuários do seed

| id | Nome | Email | Role |
|----|------|-------|------|
| 1 | Ana Souza | ana@bbts.com | REQUESTER |
| 2 | Carlos RH | carlos@bbts.com | RH |

## Vagas do seed

| id | Título | Status |
|----|--------|--------|
| 1 | Desenvolvedor Frontend Sênior | DRAFT |
| 2 | Engenheiro de Dados Pleno | PENDING_APPROVAL |
| 3 | Tech Lead Backend (Java / Spring) | APPROVED + scores calculados |

## Candidatos do seed (6)

Rodrigo Almeida · Fernanda Lima · Bruno Martins · Juliana Costa · Lucas Ferreira · Camila Rocha

---

## Motor de Score

O score é calculado no momento da aprovação da vaga:

- Cada requisito contribui proporcionalmente ao seu **peso**
- Requisitos obrigatórios ausentes aplicam **penalidade de 30%** por item
- Score final normalizado para **0–100**
- Matching case-insensitive por substring

```
score_base = (peso_atendido / peso_total) × 100
penalidade = qtd_obrigatórios_ausentes × 30%
score_final = score_base × (1 - penalidade)
```

---

## Próximas sprints

- [ ] Sprint 3: Listagem/busca de candidatos com filtros, dashboard de KPIs por vaga
- [ ] Sprint 4: Conectores externos (Gupy, Google Talent, EmpregaNet) via `ProfileConnector`
- [ ] Sprint 5: SSO / autenticação real, RBAC com role MANAGER