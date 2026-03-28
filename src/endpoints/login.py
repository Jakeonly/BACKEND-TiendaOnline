from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.usuario import Usuario  
from src.schemas.login_schema import Login
from src.utils.security import verify_password


router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/login")
def login(dato: Login, db: Session = Depends(get_db)):
    """
    Endpoint de autenticación. 
    Busca al usuario por email y verifica su contraseña hasheada.
    """
    # 1. Buscamos al usuario por su email
    user = (
        db.query(Usuario).filter(Usuario.email == dato.email).first()
    )
    
    # 2. Si no existe, error 401
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    # 3. Verificamos que la contraseña enviada coincida con el hash de la BD
    if not verify_password(dato.contraseña, user.contraseña):
        raise HTTPException(
            status_code=401, detail="Contraseña no válida para el usuario"
        )
    
    # 4. Verificamos si es administrador 
    if not user.es_admin:
        raise HTTPException(
            status_code=403, detail="Acceso restringido, el usuario no es administrador"
        )
    
    return {"resultado": "Login exitoso", "id_usuario": str(user.id)}