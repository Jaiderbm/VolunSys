from fastapi import APIRouter, HTTPException, status
from typing import List
from app.controllers import limpieza_playas_controller as controller
from app.models.limpieza_playas_model import LimpiezaPlayasCreate, LimpiezaPlayasResponse

router = APIRouter(prefix="/limpieza-playas", tags=["Limpieza de Playas"])

@router.get("/", response_model=List[LimpiezaPlayasResponse])
def obtener_todos():
    return controller.obtener_todos()

@router.get("/{id}", response_model=LimpiezaPlayasResponse)
def obtener_por_id(id: int):
    registro = controller.obtener_por_id(id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@router.post("/", response_model=LimpiezaPlayasResponse, status_code=status.HTTP_201_CREATED)
def crear(data: LimpiezaPlayasCreate):
    return controller.crear(data)

@router.put("/{id}", response_model=LimpiezaPlayasResponse)
def actualizar(id: int, data: LimpiezaPlayasCreate):
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
