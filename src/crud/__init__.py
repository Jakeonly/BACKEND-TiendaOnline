"""
Cliente CRUD que llama a los endpoints de la API.
"""
from src.crud.usuarios import (
    listar_usuarios,
    obtener_usuario,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
)
from src.crud.productos import (
    listar_productos,
    obtener_producto,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
)
from src.crud.carrito import (
    listar_carritos,
    obtener_carrito,
    crear_carrito,
    actualizar_carrito,
    eliminar_carrito,
)
from src.crud.categoria import (
    listar_categorias,
    obtener_categoria,
    crear_categoria,
    actualizar_categoria,
    eliminar_categoria,
)
from src.crud.descuento import (
    listar_descuentos,
    obtener_descuento,
    crear_descuento,
    actualizar_descuento,
    eliminar_descuento,
)
from src.crud.orden import (
    listar_ordenes,
    obtener_orden,
    crear_orden,
    actualizar_orden,
    eliminar_orden,
)
from src.crud.detalle_carrito import (
    listar_detalles_carrito,
    obtener_detalle_carrito,
    crear_detalle_carrito,
    actualizar_detalle_carrito,
    eliminar_detalle_carrito,
)
from src.crud.detalle_orden import (
    listar_detalles_orden,
    obtener_detalle_orden,
    crear_detalle_orden,
    actualizar_detalle_orden,
    eliminar_detalle_orden,
)

__all__ = [
    "listar_usuarios",
    "obtener_usuario",
    "crear_usuario",
    "actualizar_usuario",
    "eliminar_usuario",
    "listar_productos",
    "obtener_producto",
    "crear_producto",
    "actualizar_producto",
    "eliminar_producto",
    "listar_carritos",
    "obtener_carrito",
    "crear_carrito",
    "actualizar_carrito",
    "eliminar_carrito",
    "listar_categorias",
    "obtener_categoria",
    "crear_categoria",
    "actualizar_categoria",
    "eliminar_categoria",
    "listar_descuentos",
    "obtener_descuento",
    "crear_descuento",
    "actualizar_descuento",
    "eliminar_descuento",
    "listar_ordenes",
    "obtener_orden",
    "crear_orden",
    "actualizar_orden",
    "eliminar_orden",
    "listar_detalles_carrito",
    "obtener_detalle_carrito",
    "crear_detalle_carrito",
    "actualizar_detalle_carrito",
    "eliminar_detalle_carrito",
    "listar_detalles_orden",
    "obtener_detalle_orden",
    "crear_detalle_orden",
    "actualizar_detalle_orden",
    "eliminar_detalle_orden",
]
