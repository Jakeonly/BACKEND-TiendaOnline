from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.pago import Pago
from src.schemas.pago_schema import (
    PagoCreate,
    PagoUpdate,
    PagoResponse,
)
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_pagos(db: Session = Depends(get_db)):
    """Lista todos los pagos registrados."""
    db_pagos = db.query(Pago).all()
    data = [PagoResponse.model_validate(p).model_dump(mode="json") for p in db_pagos]
    return success_response(data=data, message="Lista de pagos obtenida")


@router.get("/{pago_id}")
def obtener_pago(pago_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un pago por su ID."""
    db_pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not db_pago:
        raise NotFoundError(message=f"El pago con ID {pago_id} no existe")
    data = PagoResponse.model_validate(db_pago).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    """Registra un nuevo pago asociado a una orden."""
    nuevo = Pago(**pago.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    data = PagoResponse.model_validate(nuevo).model_dump(mode="json")
    return success_response(data=data, message="Pago creado exitosamente")


@router.put("/{pago_id}")
def actualizar_pago(pago_id: UUID, pago: PagoUpdate, db: Session = Depends(get_db)):
    """Actualiza un pago existente."""
    db_pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not db_pago:
        raise NotFoundError(message="No se pudo actualizar: Pago no encontrado")

    update_data = pago.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_pago, field, value)

    db.commit()
    db.refresh(db_pago)

    data = PagoResponse.model_validate(db_pago).model_dump(mode="json")
    return success_response(data=data, message="Pago actualizado")


@router.delete("/{pago_id}", status_code=204)
def eliminar_pago(pago_id: UUID, db: Session = Depends(get_db)):
    """Elimina un pago del sistema."""
    db_pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not db_pago:
        raise NotFoundError(message="No se pudo eliminar: Pago no encontrado")

    db.delete(db_pago)
    db.commit()

    return None
