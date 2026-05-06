from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class PagoBase(BaseModel):
    monto: Decimal = Field(..., ge=0, description="Monto del pago")
    metodo: str = Field(..., max_length=50, description="Método de pago")
    estado: str = Field(default="Pendiente", max_length=20)
    orden_id: UUID = Field(..., description="ID de la orden asociada")


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    monto: Decimal | None = Field(None, ge=0)
    metodo: str | None = Field(None, max_length=50)
    estado: str | None = Field(None, max_length=20)
    orden_id: UUID | None = None


class PagoResponse(PagoBase):
    id: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
