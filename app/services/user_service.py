from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UsuarioCreate

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: UsuarioCreate):
    hashed_password = usuario.password  # Aquí deberías hashear la contraseña
    db_usuario = Usuario(username=usuario.username, nombre=usuario.nombre, email=usuario.email, hashed_password=hashed_password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
