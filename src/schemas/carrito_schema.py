from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class CarritoBase(BaseModel):
    usuario_id: UUID = Field(..., description="ID del dueño del carrito")


class CarritoCreate(CarritoBase):
    pass


class CarritoUpdate(BaseModel):
    usuario_id: UUID | None = None


class CarritoResponse(CarritoBase):
    id: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
