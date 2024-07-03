from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import IncidenteCreate, Incidente, Usuario
from app.services import incident_service
from app.db import get_db
from app.auth import get_current_user

router = APIRouter()

def es_espana(latitud: float, longitud: float):
    return 36.000104 <= latitud <= 43.791356 and -9.297189 <= longitud <= 4.354789

def temperatura_valida(temperatura: float):
    return 5 <= temperatura <= 45

@router.post("/reportar", response_model=Incidente)
async def create_incidente(incidente: IncidenteCreate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if (not current_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No puedes reportar un incidente si no estás autenticado. Por favor, inicia sesión.")
    incidente.id_usuario = current_user.id
    db_incidente = await incident_service.get_incidente_by_lat_long(db, latitud=incidente.latitud, longitud=incidente.longitud)
    if db_incidente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya hay un incidente reportado en esta ubicación.")
    if (not es_espana(incidente.latitud, incidente.longitud)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La ubicación del incidente no está en España.")
    if (not temperatura_valida(incidente.temperatura)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La temperatura no es válida. Verifique que sea correcta.")
    if (incidente.intensidad is not None and (incidente.intensidad < 0 or incidente.intensidad > 100)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La intensidad no es válida. Verifique que sea correcta.")
    if (incidente.tamano <= 0):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El tamaño no es válido. Verifique que sea correcto.")
    
    return await incident_service.create_incidente(db=db, incidente=incidente)

@router.get("/incidentes/{incidente_id}", response_model=Incidente)
def read_incidente(incidente_id: int, db: Session = Depends(get_db)):
    db_incidente = incident_service.get_incidente(db, incidente_id=incidente_id)
    if db_incidente is None:
        raise HTTPException(status_code=404, detail="Incidente not found")
    return db_incidente

#Incidentes que se busquen por latitud y longitud de los extremos del mapa

#logout del usuario
