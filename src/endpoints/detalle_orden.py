from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.detalle_orden_schema import DetalleOrdenCreate, DetalleOrdenResponse
from src.crud.detalle_orden import (
    get_detalles_orden,
    get_detalle_orden_by_id,
    create_detalle_orden,
    update_detalle_orden,
    delete_detalle_orden,
)
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_todos_los_detalles_de_ordenes(db: Session = Depends(get_db)):
    """Obtiene el desglose de todas las órdenes."""
    db_detalles = get_detalles_orden(db)
    data = [
        DetalleOrdenResponse.model_validate(d).model_dump(mode="json")
        for d in db_detalles
    ]
    return success_response(data=data, message="Detalles de órdenes obtenidos")


@router.get("/{detalle_id}")
def obtener_detalle_orden_por_id(detalle_id: UUID, db: Session = Depends(get_db)):
    """Busca un ítem de una orden por su ID."""
    db_detalle = get_detalle_orden_by_id(db, detalle_id)
    if not db_detalle:
        raise NotFoundError(message=f"Detalle con ID {detalle_id} no existe")
    data = DetalleOrdenResponse.model_validate(db_detalle).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def registrar_producto_en_orden(
    detalle: DetalleOrdenCreate, db: Session = Depends(get_db)
):
    """Registra un producto en una orden."""
    nuevo_detalle = create_detalle_orden(db=db, detalle=detalle)
    data = DetalleOrdenResponse.model_validate(nuevo_detalle).model_dump(mode="json")
    return success_response(data=data, message="Producto registrado en la orden")


@router.put("/{detalle_id}")
def actualizar_detalle_orden(
    detalle_id: UUID, detalle: DetalleOrdenCreate, db: Session = Depends(get_db)
):
    """Actualiza un ítem dentro de una orden."""
    db_detalle = update_detalle_orden(db, detalle_id, detalle)
    if not db_detalle:
        raise NotFoundError(message="No se pudo actualizar: Detalle no encontrado")
    data = DetalleOrdenResponse.model_validate(db_detalle).model_dump(mode="json")
    return success_response(data=data, message="Detalle actualizado")


@router.delete("/{detalle_id}", status_code=204)
def eliminar_detalle_orden(detalle_id: UUID, db: Session = Depends(get_db)):
    """Elimina un ítem de una orden."""
    if not delete_detalle_orden(db, detalle_id):
        raise NotFoundError(message="No se pudo eliminar: Detalle no encontrado")
    return None
