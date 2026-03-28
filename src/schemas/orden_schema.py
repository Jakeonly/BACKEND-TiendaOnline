from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class OrdenBase(BaseModel):
    total: Decimal = Field(..., ge=0, description="Monto total de la factura")
    estado: str = Field(
        default="pendiente",
        max_length=15,
        description="Estado: pendiente, pagada, cancelada",
    )
    usuario_id: UUID = Field(..., description="ID del cliente")
    descuento_id: UUID | None = Field(
        None, description="ID del descuento aplicado si existe"
    )


class OrdenCreate(OrdenBase):
    pass


class OrdenUpdate(BaseModel):
    total: Decimal | None = Field(None, ge=0)
    estado: str | None = Field(None, max_length=15)
    usuario_id: UUID | None = None
    descuento_id: UUID | None = None


class OrdenResponse(OrdenBase):
    id: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
