from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class CarritoBase(BaseModel):
    usuario_id: UUID = Field(..., description="ID del dueño del carrito")
    estado: str = Field(
        default="Pendiente", description="Estado del carrito: Pendiente o Pagado"
    )


class CarritoCreate(CarritoBase):
    estado: str = Field(
        default="Pendiente", description="Estado del carrito: Pendiente o Pagado"
    )


class CarritoUpdate(BaseModel):
    usuario_id: UUID | None = None
    estado: str | None = None


class CarritoResponse(CarritoBase):
    id: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
