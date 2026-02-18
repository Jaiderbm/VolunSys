from fastapi import APIRouter
from app.models.pais_model import PaisCreate
from app.controllers.pais_controller import crear_pais, listar_paises

router = APIRouter(prefix="/paises", tags=["Paises"])

@router.post("/")
def crear(pais: PaisCreate):
    return crear_pais(pais.nombre)

@router.get("/")
def listar():
    return listar_paises()
