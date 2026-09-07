from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    puntaje = Column(Integer, default=0)

    progresos = relationship("Progreso", back_populates="usuario")


class Leccion(Base):
    __tablename__ = "lecciones"

    id = Column(Integer, primary_key=True, index=True)
    pregunta = Column(String)
    opciones = Column(String)          # se guarda como texto JSON, ej: '["a","b","c"]'
    respuesta_correcta = Column(String)


class Progreso(Base):
    __tablename__ = "progreso"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    leccion_id = Column(Integer, ForeignKey("lecciones.id"))
    completada = Column(Boolean, default=False)

    usuario = relationship("Usuario", back_populates="progresos")
