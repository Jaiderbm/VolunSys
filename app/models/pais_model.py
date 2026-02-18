from pydantic import BaseModel

class PaisCreate(BaseModel):
    nombre: str

class PaisResponse(BaseModel):
    id: int
    nombre: str
    estado: bool
