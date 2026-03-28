from datetime import datetime
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel


# Campos comunes de la entidad producto
class ProductoBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: Decimal
    stock: int = 0
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
