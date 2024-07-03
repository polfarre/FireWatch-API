from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from enum import Enum as PyEnum

class DiaNocheEnum(PyEnum):
    dia = "DIA"
    noche = "NOCHE"

class IncidenteBase(BaseModel):
    latitud: float
    longitud: float
    intensidad: Optional[float]
    tamano: Optional[float]
    fecha_adq: datetime
    hora_adq: str
    temperatura: Optional[float]
    dia_noche: DiaNocheEnum

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

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    incidentes: List[Incidente] = []

    class Config:
        orm_mode = True
