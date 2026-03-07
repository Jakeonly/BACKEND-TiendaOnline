from datetime import datetime
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel


class DetalleCarritoBase(BaseModel):
    cantidad: int
    precio_unitario: Decimal
    carrito_id: UUID
    producto_id: UUID


class DetalleCarritoCreate(DetalleCarritoBase):
    pass


class DetalleCarritoUpdate(BaseModel):
    cantidad: int | None = None
    precio_unitario: Decimal | None = None
    carrito_id: UUID | None = None
    producto_id: UUID | None = None


class DetalleCarritoResponse(DetalleCarritoBase):
    id: UUID
    fecha_creacion: datetime | None = None

    class Config:
        from_attributes = True