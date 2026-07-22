from pydantic import BaseModel
from typing import Optional

class RescateAnimalCreate(BaseModel):
    tipo_animal: str
    condicion: Optional[str] = None
    ubicacion: Optional[str] = None
    estado: Optional[bool] = True

class RescateAnimalResponse(BaseModel):
    id: int
    tipo_animal: str
    condicion: Optional[str]
    ubicacion: Optional[str]
    estado: bool
