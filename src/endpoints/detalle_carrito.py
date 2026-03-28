from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.detalle_carrito_schema import DetalleCarritoCreate, DetalleCarritoResponse
from src.crud.detalle_carrito import (
    get_detalles_carrito,
    get_detalle_carrito_by_id,
    create_detalle_carrito,
    update_detalle_carrito,
    delete_detalle_carrito,
)
# Importamos la Capa Core
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_todos_los_detalles_de_carritos(db: Session = Depends(get_db)):
    """Obtiene todos los ítems que están dentro de los carritos."""
    db_detalles = get_detalles_carrito(db)
    return success_response(
        data=db_detalles, 
        message="Detalles de carritos obtenidos"
    )


@router.get("/{detalle_id}")
def obtener_detalle_carrito_por_id(detalle_id: str, db: Session = Depends(get_db)):
    """Busca un ítem específico de un carrito por su ID."""
    db_detalle = get_detalle_carrito_by_id(db, detalle_id)
    if not db_detalle:
        raise NotFoundError(message=f"El detalle de carrito con ID {detalle_id} no existe")
    
    return success_response(data=db_detalle)


@router.post("/")
def agregar_producto_al_carrito(
    detalle: DetalleCarritoCreate, db: Session = Depends(get_db)
):
    """Añade un producto y su cantidad a un carrito específico."""
    nuevo_detalle = create_detalle_carrito(db=db, detalle=detalle)
    return success_response(
        data=nuevo_detalle, 
        message="Producto añadido al carrito exitosamente"
    )


@router.put("/{detalle_id}")
def actualizar_cantidad_en_carrito(
    detalle_id: str, detalle: DetalleCarritoCreate, db: Session = Depends(get_db)
):
    """Modifica la cantidad de un producto ya existente en el carrito."""
    db_detalle = update_detalle_carrito(db, detalle_id, detalle)
    if not db_detalle:
        raise NotFoundError(message="No se pudo actualizar: Detalle no encontrado")
    
    return success_response(
        data=db_detalle, 
        message="Cantidad actualizada en el carrito"
    )


@router.delete("/{detalle_id}")
def quitar_producto_del_carrito(detalle_id: str, db: Session = Depends(get_db)):
    """Elimina un ítem específico del carrito."""
    exito = delete_detalle_carrito(db, detalle_id)
    if not exito:
        raise NotFoundError(message="No se pudo eliminar: Detalle no encontrado")
    
    return success_response(
        data=None, 
        message="Producto quitado del carrito"
    )