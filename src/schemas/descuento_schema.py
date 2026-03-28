from datetime import datetime
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel


class DescuentoBase(BaseModel):
    codigo: str
    porcentaje: Decimal | None = None
    monto_fijo: Decimal | None = None
    fecha_inicio: datetime
    fecha_fin: datetime


class DescuentoCreate(DescuentoBase):
    pass


class DescuentoUpdate(BaseModel):
    codigo: str | None = None
    porcentaje: Decimal | None = None
    monto_fijo: Decimal | None = None
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None


class DescuentoResponse(DescuentoBase):
    id: UUID
    fecha_creacion: datetime | None = None

    class Config:
        from_attributes = True
