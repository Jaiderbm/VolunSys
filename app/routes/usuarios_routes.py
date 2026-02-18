from fastapi import APIRouter, Depends, HTTPException
from app.controllers.usuarios_controller import (
    crear_usuario,
    listar_usuarios
)

from app.config.deps import get_current_user   # 👈 JWT

router = APIRouter()


@router.post("/")
def crear(data: dict):
    return crear_usuario(
        data["nombre"],
        data["correo"],
        data["password"],
        
        data["pais_id"],
        data["ciudad_id"]
    )


# 🔒 Ruta protegida con JWT
@router.get("/")
def listar(user=Depends(get_current_user)):
    return listar_usuarios()
