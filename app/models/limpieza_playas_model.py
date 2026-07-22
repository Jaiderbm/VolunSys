from pydantic import BaseModel
from typing import Optional

class LimpiezaPlayasCreate(BaseModel):
    nombre_playa: str
    ubicacion: Optional[str] = None
    cantidad_basura_estimada_kg: Optional[float] = None
    estado: Optional[bool] = True

class LimpiezaPlayasResponse(BaseModel):
    id: int
    nombre_playa: str
    ubicacion: Optional[str]
    cantidad_basura_estimada_kg: Optional[float]
    estado: bool
