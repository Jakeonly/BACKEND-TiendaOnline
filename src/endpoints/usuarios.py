from uuid import UUID
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
from src.core.exceptions import NotFoundError, ConflictError
from src.core.responses import success_response
from src.utils.security import hash_password  # <--- IMPORTANTE: Para cifrar la clave

router = APIRouter()


@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    """Obtiene la lista de todos los usuarios registrados."""
    db_usuarios = get_usuarios(db)
    data = [
        UsuarioResponse.model_validate(u).model_dump(mode="json") for u in db_usuarios
    ]
    return success_response(data=data, message="Lista de usuarios obtenida")


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Busca un usuario específico por su ID (UUID)."""
    db_usuario = get_usuario_by_id(db, usuario_id)
    if not db_usuario:
        raise NotFoundError(message=f"El usuario con ID {usuario_id} no existe")
    data = UsuarioResponse.model_validate(db_usuario).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_nuevo_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario verificando que el email sea único."""
    if get_usuario_by_email(db, email=usuario.email):
        raise ConflictError(message="El correo electrónico ya está registrado")

    usuario.contraseña = hash_password(usuario.contraseña)

    nuevo = create_usuario(db=db, usuario=usuario)
    data = UsuarioResponse.model_validate(nuevo).model_dump(mode="json")
    return success_response(data=data, message="Usuario registrado correctamente")


@router.put("/{usuario_id}")
def actualizar_usuario_data(
    usuario_id: UUID, usuario: UsuarioCreate, db: Session = Depends(get_db)
):
    """Actualiza la información de un usuario existente."""

    if usuario.contraseña:
        usuario.contraseña = hash_password(usuario.contraseña)

    db_usuario = update_usuario(db, usuario_id, usuario)
    if not db_usuario:
        raise NotFoundError(message="No se pudo actualizar: Usuario no encontrado")
    data = UsuarioResponse.model_validate(db_usuario).model_dump(mode="json")
    return success_response(data=data, message="Datos de usuario actualizados")


@router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario_data(usuario_id: UUID, db: Session = Depends(get_db)):
    """Elimina un usuario de la base de datos."""
    if not delete_usuario(db, usuario_id):
        raise NotFoundError(message="No se pudo eliminar: Usuario no encontrado")
    return None
