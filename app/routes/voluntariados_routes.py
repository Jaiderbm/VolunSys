from fastapi import APIRouter
from app.controllers.voluntariados_controller import get_voluntariados, crear_voluntariado, eliminar_voluntariado

router = APIRouter(prefix="/voluntariados", tags=["Voluntariados"])

@router.get("/")
def listar():
    return get_voluntariados()

@router.post("/")
def crear(data: dict):
    return crear_voluntariado(data)

@router.delete("/{id}")
def eliminar(id: int):
    return eliminar_voluntariado(id)