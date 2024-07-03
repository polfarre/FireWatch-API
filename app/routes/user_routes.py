import re
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from app.schemas import UsuarioCreate, Usuario, Token, UsuarioUpdate
from app.services import user_service
from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, authenticate_user
from app.db import get_db
from app.auth import get_current_user, get_db_internal

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = await authenticate_user(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": usuario.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/registrar", response_model=Usuario)
async def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = await user_service.get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya hay un usuario registrado con este correo electrónico.")
    db_usuario = await user_service.get_usuario_by_dni(db, dni=usuario.dni)
    if db_usuario:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya hay un usuario registrado con este DNI.")
    db_usuario = await user_service.get_usuario_by_telefono(db, telefono=usuario.telefono)
    if db_usuario:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya hay un usuario registrado con este número de teléfono.")
    db_usuario = await user_service.get_usuario_by_username(db, username=usuario.username)
    if db_usuario:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya hay un usuario registrado con este nombre de usuario.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", usuario.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El formato del correo electrónico no es válido.")
    if not re.match(r"^[679]{1}[0-9]{8}$", usuario.telefono):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El formato del número de teléfono no es válido.")
    
    return await user_service.create_usuario(db=db, usuario=usuario)

@router.put("/{usuario_id}", response_model=Usuario)
async def update_usuario(usuario_id: int, datos_nuevos: UsuarioUpdate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != usuario_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No puedes modificar la información de otro usuario.")
    
    db_usuario = await user_service.get_usuario_by_email(db, email=datos_nuevos.email)
    if db_usuario and db_usuario.id != usuario_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya hay un usuario registrado con este correo electrónico.")
    
    db_usuario = await user_service.get_usuario_by_telefono(db, telefono=datos_nuevos.telefono)
    if db_usuario and db_usuario.id != usuario_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya hay un usuario registrado con este número de teléfono.")
    
    db_usuario = await user_service.get_usuario_by_username(db, username=datos_nuevos.username)
    if db_usuario and db_usuario.id != usuario_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya hay un usuario registrado con este nombre de usuario.")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", datos_nuevos.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El formato del correo electrónico no es válido.")
    
    if not re.match(r"^[679]{1}[0-9]{8}$", datos_nuevos.telefono):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El formato del número de teléfono no es válido.")
    db_usuario = await user_service.modificar_usuario(db, usuario_id, datos_nuevos)
    return db_usuario

@router.get("/{usuario_id}", response_model=Usuario)
async def read_usuario(usuario_id: int, db: Session = Depends(get_db_internal)):
    db_usuario = await user_service.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el usuario.")
    return db_usuario

@router.delete("/{usuario_id}", response_model=Usuario)
async def delete_usuario(usuario_id: int, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db_internal)):
    db_usuario = await user_service.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha podido eliminar la cuenta correctamente.")
    
    if current_user.id != usuario_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No puedes eliminar la cuenta de otro usuario.")
    db.delete(db_usuario)
    db.commit()
    return db_usuario
