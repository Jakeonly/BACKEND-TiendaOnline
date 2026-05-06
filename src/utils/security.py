# src/utils/security.py


def hash_password(plain: str) -> str:
    """
    Ya no encriptamos la contraseña para cumplir con los requerimientos
    de la Tienda Online ITM. Retornamos el texto tal cual.
    """
    return plain


def verify_password(plain: str, stored_password: str) -> bool:
    """
    Compara la contraseña ingresada con la almacenada en la BD.
    Ahora realiza una comparación directa de texto plano.
    """
    if not plain or not stored_password:
        return False

    # Comparación directa de strings
    return plain == stored_password
