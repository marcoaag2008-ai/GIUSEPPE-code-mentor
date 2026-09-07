# main.py

import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
import gemini_service

app = FastAPI()
@app.get("/")
def inicio():
    return {"mensaje": "GIUSEPPE backend funcionando"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Chat: análisis de vulnerabilidades ----------

@app.post("/api/chat", response_model=schemas.AnalisisResponse)
async def analizar(datos: schemas.CodigoRequest):
    resultado = await gemini_service.analizar_codigo(datos.codigo)
    return {"analisis": resultado}


# ---------- Lecciones ----------

@app.get("/api/lecciones", response_model=list[schemas.LeccionOut])
def obtener_lecciones(db: Session = Depends(get_db)):
    lecciones = db.query(models.Leccion).all()

    resultado = []
    for leccion in lecciones:
        resultado.append(schemas.LeccionOut(
            id=leccion.id,
            pregunta=leccion.pregunta,
            opciones=json.loads(leccion.opciones)
        ))
    return resultado


# ---------- Progreso ----------

@app.post("/api/progreso", response_model=schemas.ProgresoOut)
def registrar_progreso(datos: schemas.ProgresoCreate, db: Session = Depends(get_db)):
    leccion = db.query(models.Leccion).filter(models.Leccion.id == datos.leccion_id).first()
    if not leccion:
        raise HTTPException(status_code=404, detail="Lección no encontrada")

    nuevo_progreso = models.Progreso(
        usuario_id=datos.usuario_id,
        leccion_id=datos.leccion_id,
        completada=datos.completada
    )
    db.add(nuevo_progreso)

    usuario = db.query(models.Usuario).filter(models.Usuario.id == datos.usuario_id).first()
    if usuario and datos.completada:
        usuario.puntaje += 10

    db.commit()
    db.refresh(nuevo_progreso)
    return nuevo_progreso


# ---------- Estadísticas ----------

@app.get("/api/estadisticas/{usuario_id}")
def obtener_estadisticas(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    completadas = db.query(models.Progreso).filter(
        models.Progreso.usuario_id == usuario_id,
        models.Progreso.completada == True
    ).count()

    return {
        "usuario": usuario.nombre,
        "puntaje": usuario.puntaje,
        "lecciones_completadas": completadas
    }
