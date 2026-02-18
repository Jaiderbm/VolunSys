from fastapi import APIRouter
from app.controllers.ciudades_controller import (
    crear_ciudad,
    listar_ciudades
)

router = APIRouter()


@router.post("/")
def crear(data: dict):
    return crear_ciudad(
        data["nombre"],
        data["pais_id"]
    )


@router.get("/")
def listar():
    return listar_ciudades()
