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
# Capa Core
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_todas_las_ordenes(db: Session = Depends(get_db)):
    """Obtiene el historial de todas las órdenes de compra."""
    db_ordenes = get_ordenes(db)
    return success_response(
        data=db_ordenes, 
        message="Historial de órdenes obtenido"
    )


@router.get("/{orden_id}")
def obtener_orden_por_id(orden_id: str, db: Session = Depends(get_db)):
    """Busca una orden específica por su identificador único."""
    db_orden = get_orden_by_id(db, orden_id)
    if not db_orden:
        raise NotFoundError(message=f"La orden con ID {orden_id} no existe")
    
    return success_response(data=db_orden)


@router.post("/")
def crear_nueva_orden_compra(orden: OrdenCreate, db: Session = Depends(get_db)):
    """Registra una nueva orden de compra en el sistema."""
    nueva_orden = create_orden(db=db, orden=orden)
    return success_response(
        data=nueva_orden, 
        message="Orden de compra creada exitosamente"
    )


@router.put("/{orden_id}")
def actualizar_estado_orden(
    orden_id: str, orden: OrdenCreate, db: Session = Depends(get_db)
):
    """Actualiza la información o estado de una orden."""
    db_orden = update_orden(db, orden_id, orden)
    if not db_orden:
        raise NotFoundError(message="No se pudo actualizar: Orden no encontrada")
    
    return success_response(
        data=db_orden, 
        message="Orden actualizada correctamente"
    )


@router.delete("/{orden_id}")
def cancelar_eliminar_orden(orden_id: str, db: Session = Depends(get_db)):
    """Elimina una orden del registro."""
    exito = delete_orden(db, orden_id)
    if not exito:
        raise NotFoundError(message="No se pudo eliminar: Orden no encontrada")
    
    return success_response(
        data=None, 
        message="Orden eliminada del sistema"
    )