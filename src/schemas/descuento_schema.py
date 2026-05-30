from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class DescuentoBase(BaseModel):
    codigo: str = Field(
        ..., min_length=3, max_length=20, description="Código del cupón (ej: PROMO2024)"
    )
    porcentaje: Decimal | None = Field(
        None, ge=0, le=100, description="Porcentaje de 0 a 100"
    )
    monto_fijo: Decimal | None = Field(
        None, ge=0, description="Descuento en valor moneda"
    )
    fecha_inicio: datetime = Field(..., description="Inicio de validez")
    fecha_fin: datetime = Field(..., description="Fin de validez")


class DescuentoCreate(DescuentoBase):
    pass


class DescuentoUpdate(BaseModel):
    codigo: str | None = Field(None, min_length=3, max_length=20)
    porcentaje: Decimal | None = Field(None, ge=0, le=100)
    monto_fijo: Decimal | None = Field(None, ge=0)
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None


class DescuentoResponse(DescuentoBase):
    id: UUID
    fecha_creacion: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
