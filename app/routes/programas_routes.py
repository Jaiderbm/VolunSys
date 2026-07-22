from fastapi import APIRouter
from app.controllers.programas_controller import (
    crear_programa,
    listar_programas,
    inscribir_usuario_programa,
    obtener_programas_usuario
)

router = APIRouter()


@router.post("/")
def crear(data: dict):
    return crear_programa(
        data["nombre"],
        data["descripcion"]
    )


@router.get("/")
def listar():
    return listar_programas()


@router.post("/inscripcion")
def inscribir(data: dict):
    return inscribir_usuario_programa(
        data["usuario_id"],
        data["programa_id"]
    )


@router.get("/mis-programas/{usuario_id}")
def mis_programas(usuario_id: int):
    return obtener_programas_usuario(usuario_id)
