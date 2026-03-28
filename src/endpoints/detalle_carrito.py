from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.detalle_carrito import DetalleCarrito
from src.entities.carrito import Carrito
from src.entities.producto import Producto
from src.schemas.detalle_carrito_schema import (
    DetalleCarritoCreate,
    DetalleCarritoUpdate,
    DetalleCarritoResponse,
)

router = APIRouter(prefix="/detalle-carrito", tags=["detalle-carrito"])


@router.get("", response_model=list[DetalleCarritoResponse])
def listar_detalles_carrito(db: Session = Depends(get_db)):
    return db.query(DetalleCarrito).all()


@router.get("/{detalle_carrito_id}", response_model=DetalleCarritoResponse)
def obtener_detalle_carrito(detalle_carrito_id: UUID, db: Session = Depends(get_db)):
    detalle = (
        db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_carrito_id).first()
    )
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle


@router.post("", response_model=DetalleCarritoResponse, status_code=201)
def crear_detalle_carrito(dato: DetalleCarritoCreate, db: Session = Depends(get_db)):
    if not db.query(Carrito).filter(Carrito.id == dato.carrito_id).first():
        raise HTTPException(status_code=400, detail="Carrito no encontrado")
    if not db.query(Producto).filter(Producto.id == dato.producto_id).first():
        raise HTTPException(status_code=400, detail="Producto no encontrado")
    detalle = DetalleCarrito(**dato.model_dump())
    db.add(detalle)
    db.commit()
    db.refresh(detalle)
    return detalle


@router.put("/{detalle_carrito_id}", response_model=DetalleCarritoResponse)
def actualizar_detalle_carrito(
    detalle_carrito_id: UUID, dato: DetalleCarritoUpdate, db: Session = Depends(get_db)
):
    detalle = (
        db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_carrito_id).first()
    )
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    for k, v in dato.model_dump(exclude_unset=True).items():
        setattr(detalle, k, v)
    db.commit()
    db.refresh(detalle)
    return detalle


@router.delete("/{detalle_carrito_id}", status_code=204)
def eliminar_detalle_carrito(detalle_carrito_id: UUID, db: Session = Depends(get_db)):
    detalle = (
        db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_carrito_id).first()
    )
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    db.delete(detalle)
    db.commit()
    return None
