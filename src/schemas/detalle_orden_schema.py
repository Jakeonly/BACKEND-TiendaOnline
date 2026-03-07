from datetime import datetime
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel


class DetalleOrdenBase(BaseModel):
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    orden_id: UUID
    producto_id: UUID


class DetalleOrdenCreate(DetalleOrdenBase):
    pass


class DetalleOrdenUpdate(BaseModel):
    cantidad: int | None = None
    precio_unitario: Decimal | None = None
    subtotal: Decimal | None = None
    orden_id: UUID | None = None
    producto_id: UUID | None = None


class DetalleOrdenResponse(DetalleOrdenBase):
    id: UUID
    fecha_creacion: datetime | None = None

    class Config:
        from_attributes = True