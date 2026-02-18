from fastapi import APIRouter
from app.controllers.inscripciones_controller import (
    crear_inscripcion,
    listar_inscripciones
)

router = APIRouter()


@router.post("/")
def crear(data: dict):
    return crear_inscripcion(
        data["usuario_id"],
        data["proyecto_id"]
    )


@router.get("/")
def listar():
    return listar_inscripciones()
