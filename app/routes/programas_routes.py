from fastapi import APIRouter
from app.controllers.programas_controller import (
    crear_programa,
    listar_programas
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
