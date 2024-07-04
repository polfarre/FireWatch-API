from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import IncendioCreate, Incendio, Usuario, IncendioUpdate
from app.services import incendio_service
from app.db import get_db
from app.auth import get_current_user

router = APIRouter()

def es_espana(latitud: float, longitud: float):
    return 36.000104 <= latitud <= 43.791356 and -9.297189 <= longitud <= 4.354789

def temperatura_valida(temperatura: float):
    return 5 <= temperatura <= 45

def intensidad_valida(intensidad: float):
    return 0 <= intensidad <= 100

#Para reportar un incendio, el usuario debe haber iniciado sesión previamente.
@router.post("/reportar", response_model=Incendio)
async def create_incendio(incendio: IncendioCreate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if (not current_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No puedes reportar un incendio si no estás autenticado. Por favor, inicia sesión.")
    incendio.id_usuario = current_user.id
    db_incendio = await incendio_service.get_incendio_by_lat_long(db, latitud=incendio.latitud, longitud=incendio.longitud)
    if db_incendio:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya hay un incendio reportado en esta ubicación.")
    if (not es_espana(incendio.latitud, incendio.longitud)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La ubicación del incendio no está en España.")
    if (not temperatura_valida(incendio.temperatura)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La temperatura no es válida. Verifique que sea correcta.")
    if (not intensidad_valida(incendio.intensidad)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La intensidad del incendio indicada no es válida. Verifique que sea correcta.")
    if (incendio.tamano <= 0):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El tamaño no es válido. Verifique que sea correcto.")
    
    return await incendio_service.post_incendio(db=db, incendio=incendio)

@router.get("/{incendio_id}", response_model=Incendio)
async def leer_incendio(incendio_id: int, db: Session = Depends(get_db)):
    db_incendio = await incendio_service.get_incendio_by_id(db, incendio_id=incendio_id)
    if db_incendio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha podido encontrar el incendio. Por favor, inténtalo de nuevo más tarde.")
    return db_incendio

@router.get("/", response_model=list[Incendio])
async def leer_incendios(db: Session = Depends(get_db)):
    return await incendio_service.get_incendios(db)

# Solo se puede modificar un incendio si eres el autor de este.
@router.put("/{incendio_id}", response_model=Incendio)
async def modificar_incendio(id: int, mod_incendio=IncendioUpdate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if (not current_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tienes que iniciar sesión para poder modificar el incendio.")
    
    db_incendio = await incendio_service.get_incendio_by_id(db, incendio_id=id)

    if (db_incendio is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ha habido un error al modificar el incendio. Por favor, inténtalo de nuevo más tarde.")

    if (db_incendio.id_usuario != current_user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No puedes modificar un incendio que no has reportado tú.")
    
    if (not temperatura_valida(mod_incendio.temperatura)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La temperatura no es válida. Verifique que sea correcta.")
    
    if (not intensidad_valida(mod_incendio.intensidad)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La intensidad del incendio indicada no es válida. Verifique que sea correcta.")
    
    if (mod_incendio.tamano <= 0):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El tamaño no es válido. Verifique que sea correcto.")

    return await incendio_service.put_incendio(db=db, incendio_id=id, datos_incendio=mod_incendio)

# Solo se puede borrar un incendio si eres el autor de este.
@router.delete("/{incendio_id}", response_model=Incendio)
async def eliminar_incendio(incendio_id: int, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if (not current_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tienes que iniciar sesión para poder eliminar el incendio.")
    
    db_incendio = await incendio_service.get_incendio_by_id(db, incendio_id=incendio_id)

    if (db_incendio.id_usuario != current_user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No puedes eliminar un incendio que no has reportado tú.")
    
    if db_incendio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ha habido un error al eliminar el incendio. Por favor, inténtalo de nuevo más tarde.")

    db.delete(db_incendio)
    db.commit()
    return db_incendio