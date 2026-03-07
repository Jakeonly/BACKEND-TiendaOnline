from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.detalle_orden import DetalleOrden
from src.schemas.detalle_orden_schema import DetalleOrdenCreate, DetalleOrdenUpdate, DetalleOrdenResponse

router = APIRouter(prefix="/detalle-orden", tags=["detalle-orden"])

@router.get("", response_model=list[DetalleOrdenResponse])
def listar_detalles(db: Session = Depends(get_db)):
    return db.query(DetalleOrden).all()

@router.get("/{detalle_id}", response_model=DetalleOrdenResponse)
def obtener_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    detalle = db.query(DetalleOrden).filter(DetalleOrden.id == detalle_id).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.post("", response_model=DetalleOrdenResponse, status_code=201)
def crear_detalle(dato: DetalleOrdenCreate, db: Session = Depends(get_db)):
    detalle = DetalleOrden(**dato.model_dump())
    db.add(detalle)
    db.commit()
    db.refresh(detalle)
    return detalle

@router.put("/{detalle_id}", response_model=DetalleOrdenResponse)
def actualizar_detalle(detalle_id: UUID, dato: DetalleOrdenUpdate, db: Session = Depends(get_db)):
    detalle = db.query(DetalleOrden).filter(DetalleOrden.id == detalle_id).first()
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
    detalle = db.query(DetalleOrden).filter(DetalleOrden.id == detalle_id).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    db.delete(detalle)
    db.commit()
    return None