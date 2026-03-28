"""
CRUD Productos
"""

from src.crud.client import _delete, _get, _post, _put


def listar_productos() -> list:
    return _get("/productos")


def obtener_producto(producto_id: str) -> dict:
    return _get(f"/productos/{producto_id}")


def crear_producto(
    nombre: str,
    precio: float,
    categoria_id: str,
    descripcion: str | None = None,
    stock: int = 0,
) -> dict:
    payload = {
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
        "categoria_id": categoria_id,
    }
    if descripcion is not None:
        payload["descripcion"] = descripcion
    return _post("/productos", json=payload)


def actualizar_producto(
    producto_id: str,
    nombre: str | None = None,
    descripcion: str | None = None,
    precio: float | None = None,
    stock: int | None = None,
    categoria_id: str | None = None,
) -> dict:
    payload = {}
    if nombre is not None:
        payload["nombre"] = nombre
    if descripcion is not None:
        payload["descripcion"] = descripcion
    if precio is not None:
        payload["precio"] = precio
    if stock is not None:
        payload["stock"] = stock
    if categoria_id is not None:
        payload["categoria_id"] = categoria_id

    return _put(f"/productos/{producto_id}", json=payload)


def eliminar_producto(producto_id: str) -> None:
    _delete(f"/productos/{producto_id}")
