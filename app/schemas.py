from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
class IncidenteBase(BaseModel):
    latitud: float
    longitud: float
    intensidad: Optional[float]
    tamano: Optional[float]
    fecha_hora_adq: datetime
    temperatura: Optional[float]

class IncidenteCreate(IncidenteBase):
    id_usuario: int

class Incidente(IncidenteBase):
    id: int
    id_usuario: int

    class Config:
        orm_mode = True

class UsuarioBase(BaseModel):
    username: str
    nombre: str
    email: EmailStr
    telefono: str
    dni: str

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

class Usuario(UsuarioBase):
    id: int
    incidentes: List[Incidente] = []

    class Config:
        orm_mode = True
