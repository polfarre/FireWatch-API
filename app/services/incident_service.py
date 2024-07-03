from sqlalchemy.orm import Session
from app.models import Incidente
from app.schemas import IncidenteCreate

def get_incidente(db: Session, incidente_id: int):
    return db.query(Incidente).filter(Incidente.id == incidente_id).first()

def get_incidentes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Incidente).offset(skip).limit(limit).all()

def create_incidente(db: Session, incidente: IncidenteCreate):
    db_incidente = Incidente(**incidente.dict())
    db.add(db_incidente)
    db.commit()
    db.refresh(db_incidente)
    return db_incidente
