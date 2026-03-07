# Endpoints FastAPI

from src.endpoints.usuarios import router as usuarios_router
from src.endpoints.categorias import router as categorias_router
from src.endpoints.productos import router as productos_router
from src.endpoints.carritos import router as carritos_router
from src.endpoints.detalle_carrito import router as detalle_carrito_router
from src.endpoints.descuentos import router as descuentos_router
from src.endpoints.ordenes import router as ordenes_router
from src.endpoints.detalle_orden import router as detalle_orden_router

__all__ = [
    "usuarios_router",
    "categorias_router",
    "productos_router",
    "carritos_router",
    "detalle_carrito_router",
    "descuentos_router",
    "ordenes_router",
    "detalle_orden_router"
]