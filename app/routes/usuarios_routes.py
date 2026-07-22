from fastapi import APIRouter
from app.controllers.usuarios_controller import *

router = APIRouter(prefix="/usuarios")

@router.get("/")
def listar():
    return get_usuarios()

@router.get("/{id}")
def get_uno(id: int):
    return get_usuario(id)

@router.get("/horas/{id}")
def get_horas(id: int):
    return {"horas_sociales": get_horas_sociales(id)}

@router.post("/")
def crear(data: dict):
    return crear_usuario(data)

@router.delete("/{id}")
def eliminar(id: int):
    return eliminar_usuario(id)

@router.put("/{id}")
def actualizar(id: int, data: dict):
    return actualizar_usuario(id, data)