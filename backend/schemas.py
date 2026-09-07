from pydantic import BaseModel
from typing import List


# ---------- Usuario ----------

class UsuarioCreate(BaseModel):
    nombre: str


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    puntaje: int

    class Config:
        from_attributes = True   # permite crear este schema a partir de un objeto SQLAlchemy


# ---------- Lección ----------

class LeccionOut(BaseModel):
    id: int
    pregunta: str
    opciones: List[str]
    # OJO: no incluimos respuesta_correcta aquí a propósito (ver explicación abajo)

    class Config:
        from_attributes = True


# ---------- Progreso ----------

class ProgresoCreate(BaseModel):
    usuario_id: int
    leccion_id: int
    completada: bool = True


class ProgresoOut(BaseModel):
    id: int
    usuario_id: int
    leccion_id: int
    completada: bool

    class Config:
        from_attributes = True


# ---------- Chat / Análisis de vulnerabilidades ----------

class CodigoRequest(BaseModel):
    codigo: str
    lenguaje: str = "python"


class AnalisisResponse(BaseModel):
    analisis: str
