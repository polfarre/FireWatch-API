from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Incendio
from app.schemas import IncendioCreate, IncendioUpdate

async def get_incendio_by_lat_long(db: Session, latitud: float, longitud: float):
    return db.query(Incendio).filter(Incendio.latitud == latitud, Incendio.longitud == longitud).first()

async def get_incendio_by_id(db: Session, incendio_id: int):
    return db.query(Incendio).filter(Incendio.id == incendio_id).first()

async def get_incendios(db: Session):
    return db.query(Incendio).all()

async def post_incendio(db: Session, incendio: IncendioCreate):
    db_incendio = Incendio(
        id_usuario=incendio.id_usuario,
        latitud=incendio.latitud,
        longitud=incendio.longitud,
        intensidad=incendio.intensidad,
        tamano=incendio.tamano,
        fecha_hora_adq=datetime.utcnow(),
        temperatura=incendio.temperatura,
    )
    db.add(db_incendio)
    db.commit()
    db.refresh(db_incendio)
    return db_incendio

async def put_incendio(db: Session, incendio_id: int, incendio_mod: IncendioUpdate):
    db_incendio = await get_incendio_by_id(db, incendio_id)
    db_incendio.intensidad = incendio_mod.intensidad
    db_incendio.tamano = incendio_mod.tamano
    db_incendio.temperatura = incendio_mod.temperatura
    db.commit()
    db.refresh(db_incendio)
    return db_incendio
