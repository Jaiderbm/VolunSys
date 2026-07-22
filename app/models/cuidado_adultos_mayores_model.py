from pydantic import BaseModel
from typing import Optional

class CuidadoAdultosMayoresCreate(BaseModel):
    nombre_adulto: str
    edad: Optional[int] = None
    condicion_medica: Optional[str] = None
    ubicacion: Optional[str] = None
    estado: Optional[bool] = True

class CuidadoAdultosMayoresResponse(BaseModel):
    id: int
    nombre_adulto: str
    edad: Optional[int]
    condicion_medica: Optional[str]
    ubicacion: Optional[str]
    estado: bool
