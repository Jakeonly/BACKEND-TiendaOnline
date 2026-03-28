from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.detalle_carrito_schema import (
    DetalleCarritoCreate,
    DetalleCarritoResponse,
)
from src.crud.detalle_carrito import (
    get_detalles_carrito,
    get_detalle_carrito_by_id,
    create_detalle_carrito,
    update_detalle_carrito,
    delete_detalle_carrito,
)
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_todos_los_detalles_de_carritos(db: Session = Depends(get_db)):
    """Obtiene todos los ítems dentro de los carritos."""
    db_detalles = get_detalles_carrito(db)
    data = [
        DetalleCarritoResponse.model_validate(d).model_dump(mode="json")
        for d in db_detalles
    ]
    return success_response(data=data, message="Detalles de carritos obtenidos")


@router.get("/{detalle_id}")
def obtener_detalle_carrito_por_id(detalle_id: UUID, db: Session = Depends(get_db)):
    """Busca un ítem de un carrito por su ID."""
    db_detalle = get_detalle_carrito_by_id(db, detalle_id)
    if not db_detalle:
        raise NotFoundError(message=f"Detalle con ID {detalle_id} no existe")
    data = DetalleCarritoResponse.model_validate(db_detalle).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def agregar_producto_al_carrito(
    detalle: DetalleCarritoCreate, db: Session = Depends(get_db)
):
    """Añade un producto al carrito."""
    nuevo_detalle = create_detalle_carrito(db=db, detalle=detalle)
    data = DetalleCarritoResponse.model_validate(nuevo_detalle).model_dump(mode="json")
    return success_response(data=data, message="Producto añadido al carrito")


@router.put("/{detalle_id}")
def actualizar_cantidad_en_carrito(
    detalle_id: UUID, detalle: DetalleCarritoCreate, db: Session = Depends(get_db)
):
    """Modifica la cantidad de un ítem en el carrito."""
    db_detalle = update_detalle_carrito(db, detalle_id, detalle)
    if not db_detalle:
        raise NotFoundError(message="No se pudo actualizar: Detalle no encontrado")
    data = DetalleCarritoResponse.model_validate(db_detalle).model_dump(mode="json")
    return success_response(data=data, message="Cantidad actualizada")


@router.delete("/{detalle_id}", status_code=204)
def quitar_producto_del_carrito(detalle_id: UUID, db: Session = Depends(get_db)):
    """Elimina un ítem específico del carrito."""
    if not delete_detalle_carrito(db, detalle_id):
        raise NotFoundError(message="No se pudo eliminar: Detalle no encontrado")
    return None
