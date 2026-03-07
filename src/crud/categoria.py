"""
CRUD Categoria
"""
from src.crud.client import _delete, _get, _post, _put


def listar_categorias() -> list:
    return _get("/categorias")


def obtener_categoria(categoria_id: str) -> dict:
    return _get(f"/categorias/{categoria_id}")


def crear_categoria(
    nombre: str,
    descripcion: str | None = None,
) -> dict:
    payload = {
        "nombre": nombre,
        "descripcion": descripcion
    }
    return _post("/categorias", json=payload)

def actualizar_categoria(
    categoria_id: str,
    nombre: str | None = None,
    descripcion: str | None = None,
) -> dict:
    payload = {}
    if nombre is not None:
        payload["nombre"] = nombre
    if descripcion is not None:
        payload["descripcion"] = descripcion
    return _put(f"/categorias/{categoria_id}", json=payload)


def eliminar_categoria(categoria_id: str) -> None:
    _delete(f"/categorias/{categoria_id}")
