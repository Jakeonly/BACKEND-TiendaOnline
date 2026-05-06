# src/utils/security.py

from __future__ import annotations

import bcrypt


def hash_password(plain: str) -> str:
    """
    Genera un hash bcrypt para la contraseña recibida.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, stored_password: str) -> bool:
    """
    Compara la contraseña ingresada con la almacenada en la BD.
    Acepta tanto texto plano legado como hashes bcrypt.
    """
    if not plain or not stored_password:
        return False

    if stored_password.startswith("$2a$") or stored_password.startswith("$2b$") or stored_password.startswith("$2y$"):
        try:
            return bcrypt.checkpw(plain.encode("utf-8"), stored_password.encode("utf-8"))
        except (ValueError, TypeError, bcrypt.error):
            return False

    return plain == stored_password