from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import IncidenteCreate, Incidente
from app.services import incident_service
from app.db import get_db

router = APIRouter()

@router.post("/incidentes/", response_model=Incidente)
def create_incidente(incidente: IncidenteCreate, db: Session = Depends(get_db)):
    return incident_service.create_incidente(db=db, incidente=incidente)

@router.get("/incidentes/{incidente_id}", response_model=Incidente)
def read_incidente(incidente_id: int, db: Session = Depends(get_db)):
    db_incidente = incident_service.get_incidente(db, incidente_id=incidente_id)
    if db_incidente is None:
        raise HTTPException(status_code=404, detail="Incidente not found")
    return db_incidente
