from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_user
from src.database.config import get_db
from src.entities.usuario import Usuario
from src.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from src.core.exceptions import NotFoundError, ConflictError
from src.core.responses import success_response
from src.utils.security import hash_password

router = APIRouter()


@router.get("/", dependencies=[Depends(get_current_user)])
def listar_usuarios_endpoint(db: Session = Depends(get_db)):
    """Obtiene la lista de todos los usuarios registrados."""
    db_usuarios = db.query(Usuario).all()
    data = [
        UsuarioResponse.model_validate(u).model_dump(mode="json") for u in db_usuarios
    ]
    return success_response(data=data, message="Lista de usuarios obtenida")


@router.get("/{usuario_id}", dependencies=[Depends(get_current_user)])
def obtener_usuario_endpoint(usuario_id: UUID, db: Session = Depends(get_db)):
    """Busca un usuario específico por su ID (UUID)."""
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise NotFoundError(message=f"El usuario con ID {usuario_id} no existe")
    data = UsuarioResponse.model_validate(db_usuario).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_nuevo_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario verificando que el email sea único."""
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise ConflictError(message="El correo electrónico ya está registrado")

    # Aplicamos el hash de seguridad
    data_in = usuario.model_dump()
    data_in["contraseña"] = hash_password(usuario.contraseña)

    nuevo = Usuario(**data_in)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    data = UsuarioResponse.model_validate(nuevo).model_dump(mode="json")
    return success_response(data=data, message="Usuario registrado correctamente")


@router.put("/{usuario_id}", dependencies=[Depends(get_current_user)])
def actualizar_usuario_data(
    usuario_id: UUID, usuario: UsuarioUpdate, db: Session = Depends(get_db)
):
    """Actualiza la información de un usuario existente."""
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise NotFoundError(message="No se pudo actualizar: Usuario no encontrado")

    update_data = usuario.model_dump(exclude_unset=True)
    if "contraseña" in update_data and update_data["contraseña"]:
        update_data["contraseña"] = hash_password(update_data["contraseña"])

    for field, value in update_data.items():
        setattr(db_usuario, field, value)

    db.commit()
    db.refresh(db_usuario)

    data = UsuarioResponse.model_validate(db_usuario).model_dump(mode="json")
    return success_response(data=data, message="Datos de usuario actualizados")


@router.delete("/{usuario_id}", status_code=204, dependencies=[Depends(get_current_user)])
def eliminar_usuario_data(usuario_id: UUID, db: Session = Depends(get_db)):
    """Elimina un usuario de la base de datos."""
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise NotFoundError(message="No se pudo eliminar: Usuario no encontrado")

    db.delete(db_usuario)
    db.commit()

    return None
