"""
CRUD DetalleCarrito
"""
from src.crud.client import _delete, _get, _post, _put


def listar_detalles_carrito() -> list:
    return _get("/detalle-carrito")


def obtener_detalle_carrito(detalle_carrito_id: str) -> dict:
    return _get(f"/detalle-carrito/{detalle_carrito_id}")


def crear_detalle_carrito(
    cantidad: int,
    precio_unitario: float,
    carrito_id: str,
    producto_id: str,
) -> dict:
    payload = {
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "carrito_id": carrito_id,
        "producto_id": producto_id,
    }
    return _post("/detalle-carrito", json=payload)


def actualizar_detalle_carrito(
    detalle_carrito_id: str,
    cantidad: int | None = None,
    precio_unitario: float | None = None,
    carrito_id: str | None = None,
    producto_id: str | None = None,
) -> dict:
    payload = {}
    if cantidad is not None:
        payload["cantidad"] = cantidad
    if precio_unitario is not None:
        payload["precio_unitario"] = precio_unitario
    if carrito_id is not None:
        payload["carrito_id"] = carrito_id
    if producto_id is not None:
        payload["producto_id"] = producto_id
    return _put(f"/detalle-carrito/{detalle_carrito_id}", json=payload)


def eliminar_detalle_carrito(detalle_carrito_id: str) -> None:
    _delete(f"/detalle-carrito/{detalle_carrito_id}")
