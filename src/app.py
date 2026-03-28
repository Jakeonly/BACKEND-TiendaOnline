"""
Aplicación FastAPI - Tienda Online ITM.
Ejecutar con:
    uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from src.core.exceptions import AppException
from src.core.error_handlers import (
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from src.core.responses import success_response
from src.database.config import Base, engine
from src.endpoints import (
    usuarios,
    productos,
    categorias,
    carritos,
    ordenes,
    descuentos,
    detalle_carrito,
    detalle_orden,
)

# Importar modelos para que Base.metadata los conozca 
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
    # Función de actualización de la BD 
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Tienda Online ITM",
    description="API con FastAPI, SQLAlchemy y PostgreSQL. Incluye manejo de errores centralizado (Capa Core) y estructuras de respuesta estándar.",
    lifespan=lifespan,
)

# Manejadores globales de excepciones 
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Registro de routers
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(productos.router, prefix="/productos", tags=["Productos"])
app.include_router(categorias.router, prefix="/categorias", tags=["Categorías"])
app.include_router(carritos.router, prefix="/carritos", tags=["Carritos"])
app.include_router(ordenes.router, prefix="/ordenes", tags=["Órdenes"])
app.include_router(descuentos.router, prefix="/descuentos", tags=["Descuentos"])
app.include_router(detalle_carrito.router, prefix="/detalle-carrito", tags=["Detalle Carrito"])
app.include_router(detalle_orden.router, prefix="/detalle-orden", tags=["Detalle Orden"])


@app.get("/")
def inicio():
    return success_response(
        data={"mensaje": "Tienda Online API", "docs": "/docs"},
        message="Bienvenido a la API de la Tienda Online",
    )