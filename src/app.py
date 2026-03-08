"""
Aplicación FastAPI. Ejecutar con:
  uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables
from src.endpoints import carritos, categorias, descuentos, detalle_carrito, detalle_orden, ordenes, productos, usuarios

# Importar modelos para que Base.metadata los conozca
import src.entities.carrito
import src.entities.categoria
import src.entities.descuento
import src.entities.detalle_carrito
import src.entities.detalle_orden
import src.entities.orden
import src.entities.producto
import src.entities.usuario


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    # shutdown si hiciera falta


app = FastAPI(
    title="API Tienda Online",
    description="API con FastAPI, SQLAlchemy y PostgreSQL",
    lifespan=lifespan,
)

app.include_router(usuarios.router)
app.include_router(productos.router)


@app.get("/")
def inicio():
    return {"mensaje": "API Tienda Online", "docs": "/docs"}