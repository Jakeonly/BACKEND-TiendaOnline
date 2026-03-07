from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.detalle_carrito import DetalleCarrito
from src.schemas.detalle_carrito_schema import DetalleCarritoCreate, DetalleCarritoUpdate, DetalleCarritoResponse

router = APIRouter(prefix="/detalle-carrito", tags=["detalle-carrito"])

@router.get("", response_model=list[DetalleCarritoResponse])
def listar_detalles(db: Session = Depends(get_db)):
    return db.query(DetalleCarrito).all()

@router.get("/{detalle_id}", response_model=DetalleCarritoResponse)
def obtener_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    detalle = db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_id).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.post("", response_model=DetalleCarritoResponse, status_code=201)
def crear_detalle(dato: DetalleCarritoCreate, db: Session = Depends(get_db)):
    detalle = DetalleCarrito(**dato.model_dump())
    db.add(detalle)
    db.commit()
    db.refresh(detalle)
    return detalle

@router.put("/{detalle_id}", response_model=DetalleCarritoResponse)
def actualizar_detalle(detalle_id: UUID, dato: DetalleCarritoUpdate, db: Session = Depends(get_db)):
    detalle = db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_id).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    update = dato.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(detalle, k, v)
    db.commit()
    db.refresh(detalle)
    return detalle

@router.delete("/{detalle_id}", status_code=204)
def eliminar_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    detalle = db.query(DetalleCarrito).filter(DetalleCarrito.id == detalle_id).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    db.delete(detalle)
    db.commit()
    return None