import re
from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioUpdate
from app.auth import get_password_hash

async def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

async def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

async def get_usuario_by_dni(db: Session, dni: str):
    return db.query(Usuario).filter(Usuario.dni == dni).first()

async def get_usuario_by_telefono(db: Session, telefono: str):
    return db.query(Usuario).filter(Usuario.telefono == telefono).first()

async def get_usuario_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()

async def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()

async def create_usuario(db: Session, usuario: UsuarioCreate):
    hashed_password = await get_password_hash(usuario.password)
    db_usuario = Usuario(username=usuario.username, nombre=usuario.nombre, email=usuario.email, hashed_password=hashed_password, dni = usuario.dni, telefono = usuario.telefono)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

async def modificar_usuario(db: Session, usuario_id: int, datos_nuevos: UsuarioUpdate):
    db_usuario = await get_usuario(db, usuario_id)
    if db_usuario is None:
        return None
    db_usuario.username = datos_nuevos.username
    db_usuario.nombre = datos_nuevos.nombre
    db_usuario.email = datos_nuevos.email
    db_usuario.telefono = datos_nuevos.telefono
    db.commit()
    db.refresh(db_usuario)
    return db_usuario