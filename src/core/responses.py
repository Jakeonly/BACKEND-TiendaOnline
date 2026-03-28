"""
Modelos de respuesta estandarizados para la API.
"""

from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiErrorDetail(BaseModel):
    """Estructura del detalle del error."""
    code: str = Field(..., description="Código interno del error")
    message: str = Field(..., description="Mensaje para el usuario")
    details: dict | list | None = Field(None, description="Detalles técnicos adicionales")


class ApiErrorResponse(BaseModel):
    """Respuesta estándar en caso de fallo."""
    success: bool = Field(False, description="Estado de la petición")
    error: ApiErrorDetail


class ApiResponse(BaseModel, Generic[T]):
    """Respuesta estándar en caso de éxito."""
    success: bool = Field(True, description="Estado de la petición")
    data: T = Field(..., description="Datos de la respuesta")
    message: str | None = Field(None, description="Mensaje informativo")


def success_response(data: Any, message: str | None = None) -> dict:
    """Genera el diccionario para respuestas exitosas."""
    return {"success": True, "data": data, "message": message}


def error_response(code: str, message: str, details: dict | list | None = None) -> dict:
    """Genera el diccionario para respuestas de error."""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details
        }
    }