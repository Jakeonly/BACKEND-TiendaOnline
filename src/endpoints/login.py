from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Any

from src.core.auth import create_access_token
from src.core.config import get_settings
from src.core.responses import error_response, success_response
from src.database.config import get_db
from src.entities.usuario import Usuario
from src.schemas.login_schema import Login
from src.utils.security import verify_password


router = APIRouter(prefix="/usuarios")

@router.post("/login")
def login(dato: Login, db: Session = Depends(get_db)) -> Any:
    """
    Endpoint de autenticación Full para la Tienda Online ITM.
    
    Lógica implementada:
    1. Acceso universal (Admin y Clientes).
    2. Validación de contraseña en texto plano.
    3. Verificación de estado de cuenta (activo).
    4. Generación de JWT con claims personalizados.
    """
    email_normalizado = dato.email.strip().lower()
    password_ingresada = dato.contraseña

    # 1. Buscamos al usuario por su email (normalizado)
    user = db.query(Usuario).filter(Usuario.email == email_normalizado).first()

    # 2. Si no existe, error 401 (Unauthorized)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=error_response(
                code="LOGIN_INVALID_CREDENTIALS",
                message="Credenciales incorrectas",
                details={"reason": "Usuario no encontrado"},
            ),
        )

    # 3. Verificamos contraseña aceptando texto plano y hashes bcrypt heredados
    if not verify_password(password_ingresada, user.contraseña):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=error_response(
                code="LOGIN_INVALID_CREDENTIALS",
                message="Credenciales incorrectas",
                details={"reason": "Contraseña no válida"},
            ),
        )

    # 4. Verificación de estado del usuario
    if not user.activo:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=error_response(
                code="LOGIN_DISABLED_ACCOUNT",
                message="Esta cuenta se encuentra desactivada. Contacte al soporte.",
            ),
        )

    # 5. Configuración y generación del Token de Acceso
    settings = get_settings()
    
    access_token = create_access_token(
        subject=str(user.id),
        email=user.email,
        es_admin=user.es_admin,
        settings=settings,
    )

    # 6. Respuesta exitosa con toda la data necesaria para el Frontend (Angular)
    return success_response(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "nombre": f"{user.nombre} {user.apellido}" if hasattr(user, 'nombre') else user.email,
                "es_admin": user.es_admin,
                "rol": "Administrador" if user.es_admin else "Cliente"
            }
        },
        message=f"¡Bienvenido {user.email}! Inicio de sesión correcto."
    )