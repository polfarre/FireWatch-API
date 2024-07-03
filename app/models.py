from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.db import Base, engine

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, unique=True, index=True, nullable=False)
    dni = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    incidentes = relationship("Incidente", back_populates="usuario")

class Incidente(Base):
    __tablename__ = "incidentes"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    intensidad = Column(Float)
    tamano = Column(Float, nullable=False)
    fecha_hora_adq = Column(DateTime)
    temperatura = Column(Float, nullable=False)

    usuario = relationship("Usuario", back_populates="incidentes")

def create_tables():
    Base.metadata.create_all(engine)