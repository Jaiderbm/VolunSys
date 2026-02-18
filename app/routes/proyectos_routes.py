from fastapi import APIRouter
from app.controllers.proyectos_controller import (
    crear_proyecto,
    listar_proyectos
)

router = APIRouter()


@router.post("/")
def crear(data: dict):
    return crear_proyecto(
        data["nombre"],
        data["programa_id"],
        data["descripcion"]
    )


@router.get("/")
def listar():
    return listar_proyectos()
