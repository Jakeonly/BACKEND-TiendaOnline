"""
CRUD DetalleOrden
"""

from src.crud.client import _delete, _get, _post, _put


def listar_detalles_orden() -> list:
    return _get("/detalle-orden")


def obtener_detalle_orden(detalle_orden_id: str) -> dict:
    return _get(f"/detalle-orden/{detalle_orden_id}")


def crear_detalle_orden(
    cantidad: int,
    precio_unitario: float,
    subtotal: float,
    orden_id: str,
    producto_id: str,
) -> dict:
    payload = {
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "subtotal": subtotal,
        "orden_id": orden_id,
        "producto_id": producto_id,
    }
    return _post("/detalle-orden", json=payload)


def actualizar_detalle_orden(
    detalle_orden_id: str,
    cantidad: int | None = None,
    precio_unitario: float | None = None,
    subtotal: float | None = None,
    orden_id: str | None = None,
    producto_id: str | None = None,
) -> dict:
    payload = {}
    if cantidad is not None:
        payload["cantidad"] = cantidad
    if precio_unitario is not None:
        payload["precio_unitario"] = precio_unitario
    if subtotal is not None:
        payload["subtotal"] = subtotal
    if orden_id is not None:
        payload["orden_id"] = orden_id
    if producto_id is not None:
        payload["producto_id"] = producto_id
    return _put(f"/detalle-orden/{detalle_orden_id}", json=payload)


def eliminar_detalle_orden(detalle_orden_id: str) -> None:
    _delete(f"/detalle-orden/{detalle_orden_id}")
