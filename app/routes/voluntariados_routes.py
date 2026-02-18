from fastapi import APIRouter
from app.controllers.voluntariados_controller import (
    crear_voluntariado,
    listar_voluntariados
)

router = APIRouter()


@router.post("/")
def crear(data: dict):
    return crear_voluntariado(
        data["usuario_id"],
        data["tipo_voluntariado_id"],
        data["fecha_inicio"],
        data.get("fecha_fin")
    )


@router.get("/")
def listar():
    return listar_voluntariados()
