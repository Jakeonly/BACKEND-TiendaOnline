from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.detalle_orden import DetalleOrden
from src.schemas.detalle_orden_schema import DetalleOrdenCreate, DetalleOrdenUpdate, DetalleOrdenResponse
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_todos_los_detalles_endpoint(db: Session = Depends(get_db)):
    """Obtiene el desglose de todas las órdenes."""
    db_detalles = db.query(DetalleOrden).all()
    data = [
        DetalleOrdenResponse.model_validate(d).model_dump(mode="json")
        for d in db_detalles
    ]
    return success_response(data=data, message="Detalles de órdenes obtenidos")


@router.get("/{detalle_id}")
def obtener_detalle_orden_endpoint(detalle_id: UUID, db: Session = Depends(get_db)):
    """Busca un ítem de una orden por su ID."""
    db_detalle = db.query(DetalleOrden).filter(DetalleOrden.id == detalle_id).first()
    if not db_detalle:
        raise NotFoundError(message=f"Detalle con ID {detalle_id} no existe")
    data = DetalleOrdenResponse.model_validate(db_detalle).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def registrar_producto_en_orden_endpoint(
    detalle: DetalleOrdenCreate, db: Session = Depends(get_db)
):
    """Registra un producto en una orden."""
    nuevo_detalle = DetalleOrden(**detalle.model_dump())
    db.add(nuevo_detalle)
    db.commit()
    db.refresh(nuevo_detalle)

    data = DetalleOrdenResponse.model_validate(nuevo_detalle).model_dump(mode="json")
    return success_response(data=data, message="Producto registrado en la orden")


@router.put("/{detalle_id}")
def actualizar_detalle_orden_endpoint(
    detalle_id: UUID, detalle: DetalleOrdenUpdate, db: Session = Depends(get_db)
):
    """Actualiza un ítem dentro de una orden."""
    db_detalle = db.query(DetalleOrden).filter(DetalleOrden.id == detalle_id).first()
    if not db_detalle:
        raise NotFoundError(message="No se pudo actualizar: Detalle no encontrado")

    for field, value in detalle.model_dump(exclude_unset=True).items():
        setattr(db_detalle, field, value)

    db.commit()
    db.refresh(db_detalle)

    data = DetalleOrdenResponse.model_validate(db_detalle).model_dump(mode="json")
    return success_response(data=data, message="Detalle actualizado")


@router.delete("/{detalle_id}", status_code=204)
def eliminar_detalle_orden_endpoint(detalle_id: UUID, db: Session = Depends(get_db)):
    """Elimina un ítem de una orden."""
    db_detalle = db.query(DetalleOrden).filter(DetalleOrden.id == detalle_id).first()
    if not db_detalle:
        raise NotFoundError(message="No se pudo eliminar: Detalle no encontrado")

    db.delete(db_detalle)
    db.commit()

    return None
