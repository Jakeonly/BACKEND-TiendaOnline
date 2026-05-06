from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.core.exceptions import NotFoundError, BadRequestError
from src.entities.descuento import Descuento
from src.entities.orden import Orden
from src.schemas.orden_schema import OrdenCreate, OrdenUpdate, OrdenResponse
from src.core.responses import success_response

router = APIRouter()


def _normalizar_fecha(valor: datetime) -> datetime:
    if valor.tzinfo is None:
        return valor
    return valor.astimezone(timezone.utc).replace(tzinfo=None)


def _aplicar_descuento(total: Decimal, descuento: Descuento) -> Decimal:
    ahora = _normalizar_fecha(datetime.now(timezone.utc))
    inicio = _normalizar_fecha(descuento.fecha_inicio)
    fin = _normalizar_fecha(descuento.fecha_fin)

    if ahora < inicio or ahora > fin:
        raise BadRequestError(
            message=f"El cupón {descuento.codigo} no está vigente en este momento"
        )

    descuento_porcentaje = Decimal("0")
    descuento_fijo = Decimal("0")

    if descuento.porcentaje is not None:
        descuento_porcentaje = total * (descuento.porcentaje / Decimal("100"))

    if descuento.monto_fijo is not None:
        descuento_fijo = descuento.monto_fijo

    descuento_aplicado = max(descuento_porcentaje, descuento_fijo)
    total_final = total - descuento_aplicado

    if total_final < 0:
        total_final = Decimal("0")

    return total_final.quantize(Decimal("0.01"))


@router.get("/")
def listar_todas_las_ordenes_endpoint(db: Session = Depends(get_db)):
    """Obtiene el historial de todas las órdenes de compra."""
    db_ordenes = db.query(Orden).all()
    data = [OrdenResponse.model_validate(o).model_dump(mode="json") for o in db_ordenes]
    return success_response(data=data, message="Historial de órdenes obtenido")


@router.get("/{orden_id}")
def obtener_orden_por_id_endpoint(orden_id: UUID, db: Session = Depends(get_db)):
    """Busca una orden específica por su identificador único."""
    db_orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not db_orden:
        raise NotFoundError(message=f"La orden con ID {orden_id} no existe")
    data = OrdenResponse.model_validate(db_orden).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_nueva_orden_compra(orden: OrdenCreate, db: Session = Depends(get_db)):
    """Registra una nueva orden de compra en el sistema."""
    payload = orden.model_dump()

    if payload.get("descuento_id") is not None:
        db_descuento = (
            db.query(Descuento).filter(Descuento.id == payload["descuento_id"]).first()
        )
        if not db_descuento:
            raise NotFoundError(message="El cupón seleccionado no existe")

        payload["total"] = _aplicar_descuento(payload["total"], db_descuento)

    nueva_orden = Orden(**payload)
    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)

    data = OrdenResponse.model_validate(nueva_orden).model_dump(mode="json")
    return success_response(data=data, message="Orden de compra creada exitosamente")


@router.put("/{orden_id}")
def actualizar_estado_orden_data(
    orden_id: UUID, orden: OrdenUpdate, db: Session = Depends(get_db)
):
    """Actualiza la información o estado de una orden."""
    db_orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not db_orden:
        raise NotFoundError(message="No se pudo actualizar: Orden no encontrada")

    update_data = orden.model_dump(exclude_unset=True)

    if update_data.get("descuento_id") is not None:
        db_descuento = (
            db.query(Descuento)
            .filter(Descuento.id == update_data["descuento_id"])
            .first()
        )
        if not db_descuento:
            raise NotFoundError(message="El cupón seleccionado no existe")

        base_total = update_data.get("total", db_orden.total)
        update_data["total"] = _aplicar_descuento(base_total, db_descuento)

    for field, value in update_data.items():
        setattr(db_orden, field, value)

    db.commit()
    db.refresh(db_orden)

    data = OrdenResponse.model_validate(db_orden).model_dump(mode="json")
    return success_response(data=data, message="Orden actualizada correctamente")


@router.delete("/{orden_id}", status_code=204)
def cancelar_eliminar_orden_data(orden_id: UUID, db: Session = Depends(get_db)):
    """Elimina una orden del registro."""
    db_orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not db_orden:
        raise NotFoundError(message="No se pudo eliminar: Orden no encontrada")

    db.delete(db_orden)
    db.commit()

    return None
