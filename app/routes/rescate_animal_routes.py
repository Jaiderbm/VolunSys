from fastapi import APIRouter, HTTPException, status
from typing import List
from app.controllers import rescate_animal_controller as controller
from app.models.rescate_animal_model import RescateAnimalCreate, RescateAnimalResponse

router = APIRouter(prefix="/rescate-animal", tags=["Rescate Animal"])

@router.get("/", response_model=List[RescateAnimalResponse])
def obtener_todos():
    return controller.obtener_todos()

@router.get("/{id}", response_model=RescateAnimalResponse)
def obtener_por_id(id: int):
    registro = controller.obtener_por_id(id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@router.post("/", response_model=RescateAnimalResponse, status_code=status.HTTP_201_CREATED)
def crear(data: RescateAnimalCreate):
    return controller.crear(data)

@router.put("/{id}", response_model=RescateAnimalResponse)
def actualizar(id: int, data: RescateAnimalCreate):
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
