from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator

class UsuarioBase(BaseModel):
    nombre_completo: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telefono: str | None = Field(None, max_length=20)
    direccion: str | None = Field(None, max_length=255)
    activo: bool = True

class UsuarioCreate(UsuarioBase):
    # Ajustamos el min_length si quieres permitir claves más cortas para pruebas
    contraseña: str = Field(..., min_length=4, max_length=100) 
    es_admin: bool = False # Valor por defecto seguro

    @field_validator("contraseña")
    @classmethod
    def contraseña_no_vacia(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("La contraseña no puede estar vacía")
        return v

class UsuarioUpdate(BaseModel):
    nombre_completo: str | None = None
    email: EmailStr | None = None
    contraseña: str | None = None # Permitir actualizar clave opcionalmente
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
        from_attributes = True # Permite mapear desde modelos de SQLAlchemy[cite: 1]