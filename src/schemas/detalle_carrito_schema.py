from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class DetalleCarritoBase(BaseModel):
    cantidad: int = Field(..., ge=1, description="La cantidad debe ser al menos 1")
    precio_unitario: Decimal = Field(
        ..., ge=0, description="Precio del producto al momento de añadir"
    )
    carrito_id: UUID = Field(..., description="ID del carrito al que pertenece")
    producto_id: UUID = Field(..., description="ID del producto añadido")


class DetalleCarritoCreate(DetalleCarritoBase):
    pass


class DetalleCarritoUpdate(BaseModel):
    cantidad: int | None = Field(None, ge=1)
    precio_unitario: Decimal | None = Field(None, ge=0)
    carrito_id: UUID | None = None
    producto_id: UUID | None = None


class DetalleCarritoResponse(DetalleCarritoBase):
    id: UUID
    fecha_creacion: datetime | None = None

    class Config:
        from_attributes = True
