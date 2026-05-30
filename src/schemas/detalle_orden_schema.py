from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class DetalleOrdenBase(BaseModel):
    cantidad: int = Field(..., ge=1)
    precio_unitario: Decimal = Field(..., ge=0)
    subtotal: Decimal = Field(..., ge=0, description="Cálculo de cantidad x precio")
    orden_id: UUID = Field(..., description="ID de la orden (factura)")
    producto_id: UUID = Field(..., description="ID del producto comprado")


class DetalleOrdenCreate(DetalleOrdenBase):
    pass


class DetalleOrdenUpdate(BaseModel):
    cantidad: int | None = Field(None, ge=1)
    precio_unitario: Decimal | None = Field(None, ge=0)
    subtotal: Decimal | None = Field(None, ge=0)
    orden_id: UUID | None = None
    producto_id: UUID | None = None


class DetalleOrdenResponse(DetalleOrdenBase):
    id: UUID
    fecha_creacion: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
