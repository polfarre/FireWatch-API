from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Incidente
from app.schemas import IncidenteCreate, Usuario

async def get_incidente_by_lat_long(db: Session, latitud: float, longitud: float):
    return db.query(Incidente).filter(Incidente.latitud == latitud, Incidente.longitud == longitud).first()

def get_incidente(db: Session, incidente_id: int):
    return db.query(Incidente).filter(Incidente.id == incidente_id).first()

def get_incidentes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Incidente).offset(skip).limit(limit).all()

async def create_incidente(db: Session, incidente: IncidenteCreate):
    db_incidente = Incidente(
        id_usuario=incidente.id_usuario,
        latitud=incidente.latitud,
        longitud=incidente.longitud,
        intensidad=incidente.intensidad,
        tamano=incidente.tamano,
        fecha_hora_adq=datetime.utcnow(),
        temperatura=incidente.temperatura,
    )
    db.add(db_incidente)
    db.commit()
    db.refresh(db_incidente)
    return db_incidente
