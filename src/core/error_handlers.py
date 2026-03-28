"""
Manejadores de eventos de excepción globales.
"""

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.exceptions import AppException
from src.core.responses import error_response


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Maneja las excepciones personalizadas de nuestra App."""
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.code, exc.message, exc.details),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Maneja excepciones estándar de FastAPI/Starlette."""
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response("HTTP_ERROR", str(exc.detail)),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Maneja errores de validación de Pydantic (422)."""
    details = [{"loc": e["loc"], "msg": e["msg"]} for e in exc.errors()]
    return JSONResponse(
        status_code=422,
        content=error_response("VALIDATION_ERROR", "Datos inválidos", details),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Captura cualquier error inesperado (500)."""
    return JSONResponse(
        status_code=500,
        content=error_response("INTERNAL_ERROR", "Ocurrió un error inesperado en el servidor."),
    )