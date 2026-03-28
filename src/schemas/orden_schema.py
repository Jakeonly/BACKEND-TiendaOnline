from datetime import datetime
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel


class OrdenBase(BaseModel):
    total: Decimal
    estado: str = "pendiente"
    usuario_id: UUID
    descuento_id: UUID | None = None


class OrdenCreate(OrdenBase):
    pass


class OrdenUpdate(BaseModel):
    total: Decimal | None = None
    estado: str | None = None
    usuario_id: UUID | None = None
    descuento_id: UUID | None = None


class OrdenResponse(OrdenBase):
    id: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
