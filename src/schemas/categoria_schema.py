from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str | None = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None


class CategoriaResponse(CategoriaBase):
    id: UUID
    fecha_creacion: datetime | None = None

    class Config:
        from_attributes = True