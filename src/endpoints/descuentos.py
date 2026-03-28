from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.descuento_schema import DescuentoCreate, DescuentoResponse

from src.crud.descuento import (
    listar_descuentos,
    obtener_descuento,
    crear_descuento,
    actualizar_descuento,
    eliminar_descuento,
)
from src.core.exceptions import NotFoundError, BadRequestError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_todos_los_descuentos_endpoint(db: Session = Depends(get_db)):
    """Obtiene la lista de todos los cupones y descuentos."""
    db_descuentos = listar_descuentos(db)
    data = [
        DescuentoResponse.model_validate(d).model_dump(mode="json")
        for d in db_descuentos
    ]
    return success_response(data=data, message="Lista de descuentos obtenida")


@router.get("/{descuento_id}")
def obtener_descuento_endpoint(descuento_id: UUID, db: Session = Depends(get_db)):
    """Busca un descuento específico por su ID."""
    db_descuento = obtener_descuento(db, descuento_id)
    if not db_descuento:
        raise NotFoundError(message=f"El descuento con ID {descuento_id} no existe")
    data = DescuentoResponse.model_validate(db_descuento).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_nuevo_descuento_endpoint(
    descuento: DescuentoCreate, db: Session = Depends(get_db)
):
    """Registra un nuevo cupón de descuento."""
    if descuento.porcentaje and descuento.porcentaje > 100:
        raise BadRequestError(message="El porcentaje no puede ser mayor a 100")

    nuevo_descuento = crear_descuento(db=db, descuento=descuento)
    data = DescuentoResponse.model_validate(nuevo_descuento).model_dump(mode="json")
    return success_response(data=data, message="Descuento creado exitosamente")


@router.put("/{descuento_id}")
def actualizar_descuento_endpoint(
    descuento_id: UUID, descuento: DescuentoCreate, db: Session = Depends(get_db)
):
    """Actualiza la información de un descuento existente."""
    db_descuento = actualizar_descuento(db, descuento_id, descuento)
    if not db_descuento:
        raise NotFoundError(message="No se pudo actualizar: Descuento no encontrado")
    data = DescuentoResponse.model_validate(db_descuento).model_dump(mode="json")
    return success_response(data=data, message="Descuento actualizado")


@router.delete("/{descuento_id}", status_code=204)
def eliminar_descuento_endpoint(descuento_id: UUID, db: Session = Depends(get_db)):
    """Elimina un descuento del sistema."""
    if not eliminar_descuento(db, descuento_id):
        raise NotFoundError(message="No se pudo eliminar: Descuento no encontrado")
    return None
