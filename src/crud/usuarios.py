"""
CRUD Usuarios - Backend (Tienda Online ITM)
Este módulo gestiona las operaciones de base de datos para los usuarios.
"""

from src.crud.client import _delete, _get, _post, _put
from src.utils.security import hash_password


def listar_usuarios() -> list:
    """Retorna la lista completa de usuarios desde la base de datos."""
    return _get("/usuarios")


def obtener_usuario(usuario_id: str) -> dict:
    """Obtiene un usuario específico por su ID."""
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
    """
    Crea un usuario nuevo.
    La contraseña se guarda como hash para evitar depender de texto plano.
    """
    payload = {
        "nombre_completo": nombre_completo,
        "email": email,
        "contraseña": hash_password(contraseña),
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
    """
    Actualiza la información de un usuario.
    Si se envía una nueva contraseña, se guarda como hash.
    """
    payload = {}

    # Solo agregamos al payload los campos que no son None para evitar sobrescribir con nulos[cite: 1]
    if nombre_completo is not None:
        payload["nombre_completo"] = nombre_completo
    if email is not None:
        payload["email"] = email
    if contraseña is not None:
        payload["contraseña"] = hash_password(contraseña)
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
    """Elimina permanentemente un usuario por su ID[cite: 1]."""
    _delete(f"/usuarios/{usuario_id}")
