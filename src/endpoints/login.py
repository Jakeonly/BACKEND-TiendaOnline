from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.auth import create_access_token
from src.core.config import get_settings
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.usuario import Usuario
from src.schemas.login_schema import Login


router = APIRouter(prefix="/usuarios")


@router.post("/login")
def login(dato: Login, db: Session = Depends(get_db)):
    """
    Endpoint de autenticación.
    Busca al usuario por email y verifica su contraseña en texto plano.
    """
    email_normalizado = dato.email.strip().lower()
    password_ingresada = dato.contraseña

    # 1. Buscamos al usuario por su email (normalizado)
    user = db.query(Usuario).filter(Usuario.email == email_normalizado).first()

    # 2. Si no existe, error 401
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # 3. Verificamos contraseña (comparación en texto plano)
    if user.contraseña != password_ingresada:
        raise HTTPException(
            status_code=401, detail="Contraseña no válida para el usuario"
        )

    if not user.activo:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    settings = get_settings()
    access_token = create_access_token(
        subject=user.id,
        email=user.email,
        es_admin=user.es_admin,
        settings=settings,
    )

    return success_response(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
            "id_usuario": str(user.id),
            "email": user.email,
            "es_admin": user.es_admin,
        },
        message="Login exitoso",
    )
