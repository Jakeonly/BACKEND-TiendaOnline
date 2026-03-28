"""
CRUD Descuento
"""

from src.crud.client import _delete, _get, _post, _put


def listar_descuentos() -> list:
    return _get("/descuentos")


def obtener_descuento(descuento_id: str) -> dict:
    return _get(f"/descuentos/{descuento_id}")


def crear_descuento(
    codigo: str,
    fecha_inicio: str,
    fecha_fin: str,
    porcentaje: float | None = None,
    monto_fijo: float | None = None,
) -> dict:
    payload = {
        "codigo": codigo,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "porcentaje": porcentaje,
        "monto_fijo": monto_fijo,
    }
    return _post("/descuentos", json=payload)


def actualizar_descuento(
    descuento_id: str,
    codigo: str | None = None,
    fecha_inicio: str | None = None,
    fecha_fin: str | None = None,
    porcentaje: float | None = None,
    monto_fijo: float | None = None,
) -> dict:
    payload = {}
    if codigo is not None:
        payload["codigo"] = codigo
    if fecha_inicio is not None:
        payload["fecha_inicio"] = fecha_inicio
    if fecha_fin is not None:
        payload["fecha_fin"] = fecha_fin
    if porcentaje is not None:
        payload["porcentaje"] = porcentaje
    if monto_fijo is not None:
        payload["monto_fijo"] = monto_fijo

    return _put(f"/descuentos/{descuento_id}", json=payload)


def eliminar_descuento(descuento_id: str) -> None:
    _delete(f"/descuentos/{descuento_id}")
