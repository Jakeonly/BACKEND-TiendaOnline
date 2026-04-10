"""
CRUD de login: conexión con los endpoints /usuarios para el logueo.
"""

from src.crud.client import _post, set_auth_token


def login(email: str, contraseña: str) -> dict:

    payload = {"email": email, "contraseña": contraseña}

    respuesta = _post("/usuarios/login", json=payload)

    if isinstance(respuesta, dict):
        token = respuesta.get("access_token")
        if isinstance(token, str) and token.strip():
            set_auth_token(token.strip())

    return respuesta
