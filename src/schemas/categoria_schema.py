from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50, description="Nombre único de la categoría")
    descripcion: str | None = Field(None, max_length=200, description="Breve descripción")

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=50)
    descripcion: str | None = Field(None, max_length=200)

class CategoriaResponse(CategoriaBase):
    id: UUID
    fecha_creacion: datetime | None = None

    class Config:
        from_attributes = True