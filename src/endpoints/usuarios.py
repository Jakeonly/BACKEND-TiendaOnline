from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from src.crud.usuarios import (
    listar_usuarios,
    obtener_usuario,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
)
from src.core.exceptions import NotFoundError, ConflictError
from src.core.responses import success_response
from src.utils.security import hash_password

router = APIRouter()


@router.get("/")
def listar_usuarios_endpoint(db: Session = Depends(get_db)):
    """Obtiene la lista de todos los usuarios registrados."""
    db_usuarios = listar_usuarios(db)
    data = [
        UsuarioResponse.model_validate(u).model_dump(mode="json") for u in db_usuarios
    ]
    return success_response(data=data, message="Lista de usuarios obtenida")


@router.get("/{usuario_id}")
def obtener_usuario_endpoint(usuario_id: UUID, db: Session = Depends(get_db)):
    """Busca un usuario específico por su ID (UUID)."""
    db_usuario = obtener_usuario(db, usuario_id)
    if not db_usuario:
        raise NotFoundError(message=f"El usuario con ID {usuario_id} no existe")
    data = UsuarioResponse.model_validate(db_usuario).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_nuevo_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario verificando que el email sea único."""
    # Nota: Aquí usamos listar_usuarios o una lógica similar para validar el email si es necesario
    db_usuarios = listar_usuarios(db)
    if any(u.email == usuario.email for u in db_usuarios):
        raise ConflictError(message="El correo electrónico ya está registrado")

    # Aplicamos el hash de seguridad
    usuario.contraseña = hash_password(usuario.contraseña)

    nuevo = crear_usuario(db=db, usuario=usuario)
    data = UsuarioResponse.model_validate(nuevo).model_dump(mode="json")
    return success_response(data=data, message="Usuario registrado correctamente")


@router.put("/{usuario_id}")
def actualizar_usuario_data(
    usuario_id: UUID, usuario: UsuarioCreate, db: Session = Depends(get_db)
):
    """Actualiza la información de un usuario existente."""
    if usuario.contraseña:
        usuario.contraseña = hash_password(usuario.contraseña)

    db_usuario = actualizar_usuario(db, usuario_id, usuario)
    if not db_usuario:
        raise NotFoundError(message="No se pudo actualizar: Usuario no encontrado")
    data = UsuarioResponse.model_validate(db_usuario).model_dump(mode="json")
    return success_response(data=data, message="Datos de usuario actualizados")


@router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario_data(usuario_id: UUID, db: Session = Depends(get_db)):
    """Elimina un usuario de la base de datos."""
    if not eliminar_usuario(db, usuario_id):
        raise NotFoundError(message="No se pudo eliminar: Usuario no encontrado")
    return None
