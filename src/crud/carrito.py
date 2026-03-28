"""
CRUD Carrito
"""

from src.crud.client import _delete, _get, _post, _put


def listar_carritos() -> list:
    return _get("/carritos")


def obtener_carrito(carrito_id: str) -> dict:
    return _get(f"/carritos/{carrito_id}")


def crear_carrito(
    usuario_id: str,
) -> dict:
    payload = {"usuario_id": usuario_id}
    return _post("/carritos", json=payload)


def actualizar_carrito(
    carrito_id: str,
    usuario_id: str | None = None,
) -> dict:
    payload = {}
    if usuario_id is not None:
        payload["usuario_id"] = usuario_id

    return _put(f"/carritos/{carrito_id}", json=payload)


def eliminar_carrito(carrito_id: str) -> None:
    _delete(f"/carritos/{carrito_id}")
