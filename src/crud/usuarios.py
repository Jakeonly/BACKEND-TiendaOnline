"""
CRUD Usuarios
"""

from src.crud.client import _delete, _get, _post, _put


def listar_usuarios() -> list:
    return _get("/usuarios")


def obtener_usuario(usuario_id: str) -> dict:
    return _get(f"/usuarios/{usuario_id}")


def crear_usuario(
    nombre_completo: str,
    email: str,
    contraseña: str,
    es_admin: bool,
    telefono: str | None = None,
    direccion: str | None = None,
    activo: bool = True,
) -> dict:
    payload = {
        "nombre_completo": nombre_completo,
        "email": email,
        "contraseña": contraseña,
        "es_admin": es_admin,
        "telefono": telefono,
        "direccion": direccion,
        "activo": activo,
    }
    return _post("/usuarios", json=payload)


def actualizar_usuario(
    usuario_id: str,
    nombre_completo: str | None = None,
    email: str | None = None,
    contraseña: str | None = None,
    es_admin: bool | None = None,
    telefono: str | None = None,
    direccion: str | None = None,
    activo: bool | None = None,
) -> dict:
    payload = {}
    if nombre_completo is not None:
        payload["nombre_completo"] = nombre_completo
    if email is not None:
        payload["email"] = email
    if contraseña is not None:
        payload["contraseña"] = contraseña
    if es_admin is not None:
        payload["es_admin"] = es_admin
    if telefono is not None:
        payload["telefono"] = telefono
    if direccion is not None:
        payload["direccion"] = direccion
    if activo is not None:
        payload["activo"] = activo

    return _put(f"/usuarios/{usuario_id}", json=payload)


def eliminar_usuario(usuario_id: str) -> None:
    _delete(f"/usuarios/{usuario_id}")
