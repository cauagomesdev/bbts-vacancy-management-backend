from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.service import require_rh
from app.imports import service
from app.imports.schemas import IntegrationLogOut

router = APIRouter(prefix="/candidates", tags=["Import (RH)"])

@router.post("/import/json", response_model=IntegrationLogOut, status_code=201, summary="Importar candidatos via JSON")
def import_json(records: list[dict], db: Session = Depends(get_db), rh: User = Depends(require_rh)):
    if not records: raise HTTPException(status_code=400, detail="Lista vazia")
    return service.import_from_json(db, records)

@router.post("/import/csv", response_model=IntegrationLogOut, status_code=201, summary="Importar candidatos via CSV")
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db), rh: User = Depends(require_rh)):
    if not file.filename.endswith(".csv"): raise HTTPException(status_code=400, detail="Arquivo deve ser .csv")
    return service.import_from_csv(db, await file.read(), filename=file.filename)

@router.get("/import/template", summary="Baixar template CSV")
def download_template(rh: User = Depends(require_rh)):
    template = "full_name,headline,email,location,linkedin_url,skills,languages,certifications,education,experiences\nJoão Silva,Dev Backend,joao@email.com,São Paulo SP,,Python:Avançado:5;FastAPI:Inter:2,Inglês:B2,AWS:Amazon:2023,USP:Ciência da Computação:Bacharelado:2018,BBTS:Dev:2022:2024:false\n"
    return PlainTextResponse(content=template, headers={"Content-Disposition": "attachment; filename=candidatos_template.csv"}, media_type="text/csv")
