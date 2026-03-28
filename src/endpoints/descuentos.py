from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.descuento_schema import DescuentoCreate, DescuentoResponse
from src.crud.descuento import (
    get_descuentos,
    get_descuento_by_id,
    create_descuento,
    update_descuento,
    delete_descuento,
)
# Capa Core
from src.core.exceptions import NotFoundError, BadRequestError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_todos_los_descuentos(db: Session = Depends(get_db)):
    """Obtiene la lista de todos los cupones y descuentos registrados."""
    db_descuentos = get_descuentos(db)
    return success_response(
        data=db_descuentos, 
        message="Lista de descuentos obtenida"
    )


@router.get("/{descuento_id}")
def obtener_descuento_por_id(descuento_id: str, db: Session = Depends(get_db)):
    """Busca un descuento específico por su ID."""
    db_descuento = get_descuento_by_id(db, descuento_id)
    if not db_descuento:
        raise NotFoundError(message=f"El descuento con ID {descuento_id} no existe")
    
    return success_response(data=db_descuento)


@router.post("/")
def crear_nuevo_descuento(descuento: DescuentoCreate, db: Session = Depends(get_db)):
    """Registra un nuevo cupón de descuento en el sistema."""
    # Ejemplo de validación de negocio usando BadRequestError
    if descuento.porcentaje and descuento.porcentaje > 100:
        raise BadRequestError(message="El porcentaje de descuento no puede ser mayor a 100")
        
    nuevo_descuento = create_descuento(db=db, descuento=descuento)
    return success_response(
        data=nuevo_descuento, 
        message="Descuento creado exitosamente"
    )


@router.put("/{descuento_id}")
def actualizar_descuento(
    descuento_id: str, descuento: DescuentoCreate, db: Session = Depends(get_db)
):
    """Actualiza la información de un descuento existente."""
    db_descuento = update_descuento(db, descuento_id, descuento)
    if not db_descuento:
        raise NotFoundError(message="No se pudo actualizar: Descuento no encontrado")
    
    return success_response(
        data=db_descuento, 
        message="Descuento actualizado correctamente"
    )


@router.delete("/{descuento_id}")
def eliminar_descuento(descuento_id: str, db: Session = Depends(get_db)):
    """Elimina un descuento del sistema."""
    exito = delete_descuento(db, descuento_id)
    if not exito:
        raise NotFoundError(message="No se pudo eliminar: Descuento no encontrado")
    
    return success_response(
        data=None, 
        message="Descuento eliminado exitosamente"
    )