"""
CRUD de login: conexión con los endpoints /usuarios para el logueo.
"""

from src.crud.client import _post


def login(email: str, contraseña: str) -> dict:

    payload = {"email": email, "contraseña": contraseña}

    respuesta = _post("/usuarios/login", json=payload)
    return respuesta
