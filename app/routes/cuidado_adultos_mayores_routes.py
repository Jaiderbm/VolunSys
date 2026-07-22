from fastapi import APIRouter, HTTPException, status
from typing import List
from app.controllers import cuidado_adultos_mayores_controller as controller
from app.models.cuidado_adultos_mayores_model import CuidadoAdultosMayoresCreate, CuidadoAdultosMayoresResponse

router = APIRouter(prefix="/cuidado-adultos-mayores", tags=["Cuidado a Adultos Mayores"])

@router.get("/", response_model=List[CuidadoAdultosMayoresResponse])
def obtener_todos():
    return controller.obtener_todos()

@router.get("/{id}", response_model=CuidadoAdultosMayoresResponse)
def obtener_por_id(id: int):
    registro = controller.obtener_por_id(id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@router.post("/", response_model=CuidadoAdultosMayoresResponse, status_code=status.HTTP_201_CREATED)
def crear(data: CuidadoAdultosMayoresCreate):
    return controller.crear(data)

@router.put("/{id}", response_model=CuidadoAdultosMayoresResponse)
def actualizar(id: int, data: CuidadoAdultosMayoresCreate):
    registro = controller.obtener_por_id(id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return controller.actualizar(id, data)

@router.delete("/{id}")
def eliminar(id: int):
    registro = controller.obtener_por_id(id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return controller.eliminar(id)
