from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.orden import Orden
from src.entities.usuario import Usuario
from src.entities.descuento import Descuento
from src.schemas.orden_schema import OrdenCreate, OrdenUpdate, OrdenResponse

router = APIRouter(prefix="/ordenes", tags=["ordenes"])

@router.get("", response_model=list[OrdenResponse])
def listar_ordenes(db: Session = Depends(get_db)):
    return db.query(Orden).all()

@router.get("/{orden_id}", response_model=OrdenResponse)
def obtener_orden(orden_id: UUID, db: Session = Depends(get_db)):
    orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return orden

@router.post("", response_model=OrdenResponse, status_code=201)
def crear_orden(dato: OrdenCreate, db: Session = Depends(get_db)):
    if not db.query(Usuario).filter(Usuario.id == dato.usuario_id).first():
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    if dato.descuento_id:
        if not db.query(Descuento).filter(Descuento.id == dato.descuento_id).first():
            raise HTTPException(status_code=400, detail="Descuento no encontrado")
    orden = Orden(**dato.model_dump())
    db.add(orden)
    db.commit()
    db.refresh(orden)
    return orden

@router.put("/{orden_id}", response_model=OrdenResponse)
def actualizar_orden(orden_id: UUID, dato: OrdenUpdate, db: Session = Depends(get_db)):
    orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    for k, v in dato.model_dump(exclude_unset=True).items():
        setattr(orden, k, v)
    db.commit()
    db.refresh(orden)
    return orden

@router.delete("/{orden_id}", status_code=204)
def eliminar_orden(orden_id: UUID, db: Session = Depends(get_db)):
    orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    db.delete(orden)
    db.commit()
    return None