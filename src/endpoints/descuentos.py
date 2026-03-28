from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.descuento import Descuento
from src.schemas.descuento_schema import (
    DescuentoCreate,
    DescuentoUpdate,
    DescuentoResponse,
)

router = APIRouter(prefix="/descuentos", tags=["descuentos"])


@router.get("", response_model=list[DescuentoResponse])
def listar_descuentos(db: Session = Depends(get_db)):
    return db.query(Descuento).all()


@router.get("/{descuento_id}", response_model=DescuentoResponse)
def obtener_descuento(descuento_id: UUID, db: Session = Depends(get_db)):
    descuento = db.query(Descuento).filter(Descuento.id == descuento_id).first()
    if not descuento:
        raise HTTPException(status_code=404, detail="Descuento no encontrado")
    return descuento


@router.post("", response_model=DescuentoResponse, status_code=201)
def crear_descuento(dato: DescuentoCreate, db: Session = Depends(get_db)):
    if db.query(Descuento).filter(Descuento.codigo == dato.codigo).first():
        raise HTTPException(status_code=400, detail="Código de descuento ya existe")
    descuento = Descuento(**dato.model_dump())
    db.add(descuento)
    db.commit()
    db.refresh(descuento)
    return descuento


@router.put("/{descuento_id}", response_model=DescuentoResponse)
def actualizar_descuento(
    descuento_id: UUID, dato: DescuentoUpdate, db: Session = Depends(get_db)
):
    descuento = db.query(Descuento).filter(Descuento.id == descuento_id).first()
    if not descuento:
        raise HTTPException(status_code=404, detail="Descuento no encontrado")
    for k, v in dato.model_dump(exclude_unset=True).items():
        setattr(descuento, k, v)
    db.commit()
    db.refresh(descuento)
    return descuento


@router.delete("/{descuento_id}", status_code=204)
def eliminar_descuento(descuento_id: UUID, db: Session = Depends(get_db)):
    descuento = db.query(Descuento).filter(Descuento.id == descuento_id).first()
    if not descuento:
        raise HTTPException(status_code=404, detail="Descuento no encontrado")
    db.delete(descuento)
    db.commit()
    return None
