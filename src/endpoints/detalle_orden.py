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
# Importamos la Capa Core
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_todos_los_detalles_de_ordenes(db: Session = Depends(get_db)):
    """Obtiene el desglose de productos de todas las órdenes."""
    db_detalles = get_detalles_orden(db)
    return success_response(
        data=db_detalles, 
        message="Detalles de órdenes obtenidos correctamente"
    )


@router.get("/{detalle_id}")
def obtener_detalle_orden_por_id(detalle_id: str, db: Session = Depends(get_db)):
    """Busca un ítem específico de una orden por su ID."""
    db_detalle = get_detalle_orden_by_id(db, detalle_id)
    if not db_detalle:
        raise NotFoundError(message=f"El detalle de orden con ID {detalle_id} no existe")
    
    return success_response(data=db_detalle)


@router.post("/")
def registrar_producto_en_orden(
    detalle: DetalleOrdenCreate, db: Session = Depends(get_db)
):
    """Registra un producto, su cantidad y precio en una orden específica."""
    nuevo_detalle = create_detalle_orden(db=db, detalle=detalle)
    return success_response(
        data=nuevo_detalle, 
        message="Producto registrado en la orden con éxito"
    )


@router.put("/{detalle_id}")
def actualizar_detalle_orden(
    detalle_id: str, detalle: DetalleOrdenCreate, db: Session = Depends(get_db)
):
    """Actualiza la información de un ítem dentro de una orden."""
    db_detalle = update_detalle_orden(db, detalle_id, detalle)
    if not db_detalle:
        raise NotFoundError(message="No se pudo actualizar: Detalle de orden no encontrado")
    
    return success_response(
        data=db_detalle, 
        message="Detalle de orden actualizado"
    )


@router.delete("/{detalle_id}")
def eliminar_detalle_orden(detalle_id: str, db: Session = Depends(get_db)):
    """Elimina un ítem de una orden específica."""
    exito = delete_detalle_orden(db, detalle_id)
    if not exito:
        raise NotFoundError(message="No se pudo eliminar: Detalle de orden no encontrado")
    
    return success_response(
        data=None, 
        message="Detalle de orden eliminado"
    )