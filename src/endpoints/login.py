from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from src.core.auth import create_access_token
from src.core.config import get_settings
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.usuario import Usuario
from src.schemas.login_schema import Login


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
        raise HTTPException(
            status_code=401, 
            detail="Credenciales incorrectas: Usuario no encontrado"
        )

    # 3. Verificamos contraseña (hash actual y fallback legacy)
    password_ok = verify_password(password_ingresada, user.contraseña)

    if not password_ok and user.contraseña == password_ingresada:
        # Usuario legacy con contraseña en texto plano: auto-migramos a hash
        from src.utils.security import hash_password

        user.contraseña = hash_password(password_ingresada)
        db.commit()
        db.refresh(user)
        password_ok = True

    if not password_ok:
        raise HTTPException(
            status_code=401, 
            detail="Credenciales incorrectas: Contraseña no válida"
        )

    # 4. Verificación de estado del usuario
    if not user.activo:
        raise HTTPException(
            status_code=403, 
            detail="Esta cuenta se encuentra desactivada. Contacte al soporte."
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