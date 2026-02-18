from fastapi import APIRouter
from app.controllers.tipos_voluntariado_controller import (
    crear_tipo,
    listar_tipos
)

router = APIRouter()


@router.post("/")
def crear(data: dict):
    return crear_tipo(
        data["nombre"],
        data["descripcion"]
    )


@router.get("/")
def listar():
    return listar_tipos()
