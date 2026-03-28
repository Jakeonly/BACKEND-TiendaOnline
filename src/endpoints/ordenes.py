from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.orden_schema import OrdenCreate, OrdenResponse
from src.crud.orden import (
    get_ordenes,
    get_orden_by_id,
    create_orden,
    update_orden,
    delete_orden,
)
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_todas_las_ordenes(db: Session = Depends(get_db)):
    """Obtiene el historial de todas las órdenes de compra."""
    db_ordenes = get_ordenes(db)
    data = [OrdenResponse.model_validate(o).model_dump(mode="json") for o in db_ordenes]
    return success_response(data=data, message="Historial de órdenes obtenido")


@router.get("/{orden_id}")
def obtener_orden_por_id(orden_id: UUID, db: Session = Depends(get_db)):
    """Busca una orden específica por su identificador único."""
    db_orden = get_orden_by_id(db, orden_id)
    if not db_orden:
        raise NotFoundError(message=f"La orden con ID {orden_id} no existe")
    data = OrdenResponse.model_validate(db_orden).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_nueva_orden_compra(orden: OrdenCreate, db: Session = Depends(get_db)):
    """Registra una nueva orden de compra en el sistema."""
    nueva_orden = create_orden(db=db, orden=orden)
    data = OrdenResponse.model_validate(nueva_orden).model_dump(mode="json")
    return success_response(data=data, message="Orden de compra creada exitosamente")


@router.put("/{orden_id}")
def actualizar_estado_orden(
    orden_id: UUID, orden: OrdenCreate, db: Session = Depends(get_db)
):
    """Actualiza la información o estado de una orden."""
    db_orden = update_orden(db, orden_id, orden)
    if not db_orden:
        raise NotFoundError(message="No se pudo actualizar: Orden no encontrada")
    data = OrdenResponse.model_validate(db_orden).model_dump(mode="json")
    return success_response(data=data, message="Orden actualizada correctamente")


@router.delete("/{orden_id}", status_code=204)
def cancelar_eliminar_orden(orden_id: UUID, db: Session = Depends(get_db)):
    """Elimina una orden del registro."""
    if not delete_orden(db, orden_id):
        raise NotFoundError(message="No se pudo eliminar: Orden no encontrada")
    return None
