from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from src.crud.usuarios import (
    get_usuarios,
    get_usuario_by_id,
    get_usuario_by_email,
    create_usuario,
    update_usuario,
    delete_usuario,
)
# Importamos las herramientas de la Capa Core
from src.core.exceptions import NotFoundError, ConflictError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    """Obtiene la lista de todos los usuarios registrados."""
    db_usuarios = get_usuarios(db)
    return success_response(
        data=db_usuarios, 
        message="Lista de usuarios obtenida exitosamente"
    )


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: str, db: Session = Depends(get_db)):
    """Busca un usuario específico por su ID."""
    db_usuario = get_usuario_by_id(db, usuario_id)
    if not db_usuario:
        raise NotFoundError(message=f"El usuario con ID {usuario_id} no existe")
    
    return success_response(data=db_usuario)


@router.post("/")
def crear_nuevo_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario verificando que el email sea único."""
    db_usuario = get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise ConflictError(message="El correo electrónico ya está registrado")
    
    nuevo_usuario = create_usuario(db=db, usuario=usuario)
    return success_response(
        data=nuevo_usuario, 
        message="Usuario registrado correctamente"
    )


@router.put("/{usuario_id}")
def actualizar_usuario_data(
    usuario_id: str, usuario: UsuarioCreate, db: Session = Depends(get_db)
):
    """Actualiza la información de un usuario existente."""
    db_usuario = update_usuario(db, usuario_id, usuario)
    if not db_usuario:
        raise NotFoundError(message="No se pudo actualizar: Usuario no encontrado")
    
    return success_response(
        data=db_usuario, 
        message="Datos de usuario actualizados"
    )


@router.delete("/{usuario_id}")
def eliminar_usuario_data(usuario_id: str, db: Session = Depends(get_db)):
    """Elimina un usuario de la base de datos."""
    exito = delete_usuario(db, usuario_id)
    if not exito:
        raise NotFoundError(message="No se pudo eliminar: Usuario no encontrado")
    
    return success_response(
        data=None, 
        message="Usuario eliminado exitosamente"
    )