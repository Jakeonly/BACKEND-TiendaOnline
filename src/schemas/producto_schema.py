from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from uuid import UUID

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: str | None = Field(None, max_length=500)
    precio: Decimal = Field(..., gt=0) # Debe ser mayor a 0
    stock: int = Field(default=0, ge=0) # No puede ser negativo
    categoria_id: UUID


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    precio: Decimal | None = None
    stock: int | None = None
    categoria_id: UUID | None = None


class ProductoResponse(ProductoBase):
    id: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
