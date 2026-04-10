from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.detalle_carrito_schema import (
    DetalleCarritoCreate,
    DetalleCarritoUpdate,
    DetalleCarritoResponse,
)
from src.entities.detalle_carrito import DetalleCarrito
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_todos_los_detalles_endpoint(db: Session = Depends(get_db)):
    """Obtiene todos los ítems dentro de los carritos."""
    db_detalles = db.query(DetalleCarrito).all()
    data = [
        DetalleCarritoResponse.model_validate(d).model_dump(mode="json")
        for d in db_detalles
    ]
    return success_response(data=data, message="Detalles de carritos obtenidos")


@router.get("/{detalle_id}")
def obtener_detalle_carrito_endpoint(detalle_id: UUID, db: Session = Depends(get_db)):
    """Busca un ítem de un carrito por su ID."""
    db_detalle = db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_id).first()
    if not db_detalle:
        raise NotFoundError(message=f"Detalle con ID {detalle_id} no existe")
    data = DetalleCarritoResponse.model_validate(db_detalle).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def agregar_producto_al_carrito_endpoint(
    detalle: DetalleCarritoCreate, db: Session = Depends(get_db)
):
    """Añade un producto al carrito."""
    nuevo_detalle = DetalleCarrito(**detalle.model_dump())
    db.add(nuevo_detalle)
    db.commit()
    db.refresh(nuevo_detalle)

    data = DetalleCarritoResponse.model_validate(nuevo_detalle).model_dump(mode="json")
    return success_response(data=data, message="Producto añadido al carrito")


@router.put("/{detalle_id}")
def actualizar_cantidad_en_carrito_endpoint(
    detalle_id: UUID, detalle: DetalleCarritoUpdate, db: Session = Depends(get_db)
):
    """Modifica la cantidad de un ítem en el carrito."""
    db_detalle = db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_id).first()
    if not db_detalle:
        raise NotFoundError(message="No se pudo actualizar: Detalle no encontrado")

    for field, value in detalle.model_dump(exclude_unset=True).items():
        setattr(db_detalle, field, value)

    db.commit()
    db.refresh(db_detalle)

    data = DetalleCarritoResponse.model_validate(db_detalle).model_dump(mode="json")
    return success_response(data=data, message="Cantidad actualizada")


@router.delete("/{detalle_id}", status_code=204)
def quitar_producto_del_carrito_endpoint(
    detalle_id: UUID, db: Session = Depends(get_db)
):
    """Elimina un ítem específico del carrito."""
    db_detalle = db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_id).first()
    if not db_detalle:
        raise NotFoundError(message="No se pudo eliminar: Detalle no encontrado")

    db.delete(db_detalle)
    db.commit()

    return None
