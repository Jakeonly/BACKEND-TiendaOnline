"""
CRUD Orden
"""
from src.crud.client import _delete, _get, _post, _put


def listar_ordenes() -> list:
    return _get("/ordenes")


def obtener_orden(orden_id: str) -> dict:
    return _get(f"/ordenes/{orden_id}")


def crear_orden(
    total: float,
    usuario_id: str,
    estado: str = "pendiente",
    descuento_id: str | None = None,
) -> dict:
    payload = {
        "total": total,
        "usuario_id": usuario_id,
        "estado": estado,
        "descuento_id": descuento_id, 
    }
    return _post("/ordenes", json=payload)

def actualizar_orden(
    orden_id: str,
    total: float | None = None,
    usuario_id: str | None = None,
    estado: str | None = None,
    descuento_id: str | None = None,
) -> dict:
    payload = {}
    if total is not None:
        payload["total"] = total
    if usuario_id is not None:
        payload["usuario_id"] = usuario_id
    if estado is not None:
        payload["estado"] = estado
    if descuento_id is not None:
        payload["descuento_id"] = descuento_id

    return _put(f"/ordenes/{orden_id}", json=payload)


def eliminar_orden(orden_id: str) -> None:
    _delete(f"/ordenes/{orden_id}")
