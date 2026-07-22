from fastapi import APIRouter
from app.controllers.inscripciones_controller import crear_inscripcion

router = APIRouter(prefix="/inscripciones")

@router.get("/")
def listar():
    from app.controllers.inscripciones_controller import get_inscripciones
    return get_inscripciones()

@router.post("/")
def crear(data: dict):
    return crear_inscripcion(data)

@router.post("/confirmar/{id}")
def confirmar(id: int, data: dict = None):
    horas = data.get("horas", 4) if data else 4
    from app.controllers.inscripciones_controller import confirmar_asistencia
    return confirmar_asistencia(id, horas)

@router.post("/asignar/{id}")
def asignar(id: int, data: dict):
    tarea = data.get("tarea", "")
    from app.controllers.inscripciones_controller import asignar_tarea
    return asignar_tarea(id, tarea)