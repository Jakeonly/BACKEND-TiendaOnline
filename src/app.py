"""
Aplicación FastAPI. Ejecutar con:
  uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables

# Importamos los routers de la carpeta endpoints
from src.endpoints import (
    carritos,
    categorias,
    descuentos,
    detalle_carrito,
    detalle_orden,
    ordenes,
    productos,
    usuarios,
)

# Importar modelos para que Base.metadata los conozca al crear las tablas
import src.entities  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="API Tienda Online - Proyecto ITM",
    description="API con FastAPI, SQLAlchemy y PostgreSQL para gestión de e-commerce",
    lifespan=lifespan,
)

# REGISTRO DE TODOS LOS ROUTERS (Los 8 deben estar aquí)
app.include_router(usuarios.router)
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(carritos.router)
app.include_router(descuentos.router)
app.include_router(ordenes.router)
app.include_router(detalle_carrito.router)
app.include_router(detalle_orden.router)


@app.get("/")
def inicio():
    return {
        "success": True,
        "data": {
            "mensaje": "API Tienda Online lista",
            "documentacion": "/docs",
            "redoc": "/redoc",
        },
    }
