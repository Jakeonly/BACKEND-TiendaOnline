from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.detalle_carrito_schema import (
    DetalleCarritoCreate,
    DetalleCarritoUpdate,
    DetalleCarritoResponse,
)
from src.entities.producto import Producto
from src.entities.detalle_carrito import DetalleCarrito
from src.core.exceptions import NotFoundError
from src.core.exceptions import InsufficientStockError
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


@router.get("/carrito/{carrito_id}")
def obtener_detalles_por_carrito_endpoint(
    carrito_id: UUID, db: Session = Depends(get_db)
):
    """Obtiene todos los ítems de un carrito específico."""
    db_detalles = (
        db.query(DetalleCarrito).filter(DetalleCarrito.carrito_id == carrito_id).all()
    )
    data = [
        DetalleCarritoResponse.model_validate(d).model_dump(mode="json")
        for d in db_detalles
    ]
    return success_response(data=data, message="Detalles del carrito obtenidos")


@router.get("/{detalle_id}")
def obtener_detalle_carrito_endpoint(detalle_id: UUID, db: Session = Depends(get_db)):
    """Busca un ítem de un carrito por su ID."""
    db_detalle = (
        db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_id).first()
    )
    if not db_detalle:
        raise NotFoundError(message=f"Detalle con ID {detalle_id} no existe")
    data = DetalleCarritoResponse.model_validate(db_detalle).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def agregar_producto_al_carrito_endpoint(
    detalle: DetalleCarritoCreate, db: Session = Depends(get_db)
):
    """Añade un producto al carrito."""
    db_producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
    if not db_producto:
        raise NotFoundError(message=f"Producto con ID {detalle.producto_id} no existe")

    if int(db_producto.stock or 0) < int(detalle.cantidad):
        raise InsufficientStockError(
            message=f"El producto {db_producto.nombre} no tiene stock suficiente"
        )

    db_producto.stock = int(db_producto.stock or 0) - int(detalle.cantidad)
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
    db_detalle = (
        db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_id).first()
    )
    if not db_detalle:
        raise NotFoundError(message="No se pudo actualizar: Detalle no encontrado")

    producto_anterior = (
        db.query(Producto).filter(Producto.id == db_detalle.producto_id).first()
    )
    if not producto_anterior:
        raise NotFoundError(
            message=f"Producto con ID {db_detalle.producto_id} no existe"
        )

    update_data = detalle.model_dump(exclude_unset=True)
    nuevo_producto_id = update_data.get("producto_id", db_detalle.producto_id)
    nueva_cantidad = int(update_data.get("cantidad", db_detalle.cantidad))

    if nuevo_producto_id == db_detalle.producto_id:
        diferencia = nueva_cantidad - int(db_detalle.cantidad)
        if diferencia > 0:
            if int(producto_anterior.stock or 0) < diferencia:
                raise InsufficientStockError(
                    message=f"El producto {producto_anterior.nombre} no tiene stock suficiente"
                )
            producto_anterior.stock = int(producto_anterior.stock or 0) - diferencia
        elif diferencia < 0:
            producto_anterior.stock = int(producto_anterior.stock or 0) + abs(diferencia)
    else:
        producto_anterior.stock = int(producto_anterior.stock or 0) + int(db_detalle.cantidad)

        producto_nuevo = db.query(Producto).filter(Producto.id == nuevo_producto_id).first()
        if not producto_nuevo:
                        raise NotFoundError(message=f"Producto con ID {nuevo_producto_id} no existe")

        if int(producto_nuevo.stock or 0) < nueva_cantidad:
            raise InsufficientStockError(
                message=f"El producto {producto_nuevo.nombre} no tiene stock suficiente"
            )

        producto_nuevo.stock = int(producto_nuevo.stock or 0) - nueva_cantidad

    for field, value in update_data.items():
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
    db_detalle = (
        db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_id).first()
    )
    if not db_detalle:
        raise NotFoundError(message="No se pudo eliminar: Detalle no encontrado")

    db_producto = db.query(Producto).filter(Producto.id == db_detalle.producto_id).first()
    if not db_producto:
        raise NotFoundError(
            message=f"Producto con ID {db_detalle.producto_id} no existe"
        )

    db_producto.stock = int(db_producto.stock or 0) + int(db_detalle.cantidad)

    db.delete(db_detalle)
    db.commit()

    return None
