from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.carrito import Carrito
from src.entities.usuario import Usuario
from src.schemas.carrito_schema import CarritoCreate, CarritoUpdate, CarritoResponse

router = APIRouter(prefix="/carritos", tags=["carritos"])


@router.get("", response_model=list[CarritoResponse])
def listar_carritos(db: Session = Depends(get_db)):
    return db.query(Carrito).all()


@router.get("/{carrito_id}", response_model=CarritoResponse)
def obtener_carrito(carrito_id: UUID, db: Session = Depends(get_db)):
    carrito = db.query(Carrito).filter(Carrito.id == carrito_id).first()
    if not carrito:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    return carrito


@router.post("", response_model=CarritoResponse, status_code=201)
def crear_carrito(dato: CarritoCreate, db: Session = Depends(get_db)):
    if not db.query(Usuario).filter(Usuario.id == dato.usuario_id).first():
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    carrito = Carrito(**dato.model_dump())
    db.add(carrito)
    db.commit()
    db.refresh(carrito)
    return carrito


@router.put("/{carrito_id}", response_model=CarritoResponse)
def actualizar_carrito(
    carrito_id: UUID, dato: CarritoUpdate, db: Session = Depends(get_db)
):
    carrito = db.query(Carrito).filter(Carrito.id == carrito_id).first()
    if not carrito:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    for k, v in dato.model_dump(exclude_unset=True).items():
        setattr(carrito, k, v)
    db.commit()
    db.refresh(carrito)
    return carrito


@router.delete("/{carrito_id}", status_code=204)
def eliminar_carrito(carrito_id: UUID, db: Session = Depends(get_db)):
    carrito = db.query(Carrito).filter(Carrito.id == carrito_id).first()
    if not carrito:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    db.delete(carrito)
    db.commit()
    return None
