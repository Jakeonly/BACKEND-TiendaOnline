from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


# Campos comunes de la entidad usuario
class UsuarioBase(BaseModel):
    nombre_completo: str
    email: EmailStr
    telefono: str | None = None
    direccion: str | None = None
    activo: bool = True


# Campos añadidos al ejecutar un create
class UsuarioCreate(UsuarioBase):
    contraseña: str
    es_admin: bool


# Campos modificables en un update
class UsuarioUpdate(BaseModel):
    nombre_completo: str | None = None
    email: EmailStr | None = None
    contraseña: str | None = None
    telefono: str | None = None
    direccion: str | None = None
    activo: bool | None = None
    es_admin: bool | None = None


class UsuarioResponse(UsuarioBase):
    id: UUID
    es_admin: bool | None = None
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
