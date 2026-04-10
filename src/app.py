"""
Aplicación FastAPI - Tienda Online ITM.
Ejecutar con:
    uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.core.exceptions import AppException
from src.core.error_handlers import (
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from src.core.config import get_settings
from src.core.responses import success_response
from src.database.config import create_tables
from src.endpoints import (
    login,
    usuarios,
    productos,
    categorias,
    carritos,
    ordenes,
    descuentos,
    detalle_carrito,
    detalle_orden,
)

# Importar modelos para que SQLAlchemy los reconozca al crear tablas
import src.entities.usuario  # noqa: F401
import src.entities.producto  # noqa: F401
import src.entities.categoria  # noqa: F401
import src.entities.carrito  # noqa: F401
import src.entities.orden  # noqa: F401
import src.entities.descuento  # noqa: F401
import src.entities.detalle_carrito  # noqa: F401
import src.entities.detalle_orden  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida de la aplicación: crea tablas al iniciar."""
    create_tables()
    yield


app = FastAPI(
    title="Tienda Online ITM",
    description="API con FastAPI, SQLAlchemy y PostgreSQL. Manejo de errores centralizado y seguridad HASH.",
    lifespan=lifespan,
)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# Manejadores globales de excepciones (Capa Core)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Registro de routers - Sincronizados con src.endpoints.__init__
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(productos.router, prefix="/productos", tags=["Productos"])
app.include_router(categorias.router, prefix="/categorias", tags=["Categorías"])
app.include_router(carritos.router, prefix="/carritos", tags=["Carritos"])
app.include_router(ordenes.router, prefix="/ordenes", tags=["Órdenes"])
app.include_router(descuentos.router, prefix="/descuentos", tags=["Descuentos"])
app.include_router(
    detalle_carrito.router, prefix="/detalle-carrito", tags=["Detalle Carrito"]
)
app.include_router(
    detalle_orden.router, prefix="/detalle-orden", tags=["Detalle Orden"]
)
app.include_router(login.router, tags=["Autenticación"])


@app.get("/")
def inicio():
    """Endpoint de bienvenida y salud de la API."""
    return success_response(
        data={"mensaje": "Tienda Online API", "docs": "/docs"},
        message="Bienvenido a la API de la Tienda Online",
    )
