from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.carrito_schema import CarritoCreate, CarritoResponse
from src.crud.carrito import (
    get_carritos,
    get_carrito_by_id,
    create_carrito,
    update_carrito,
    delete_carrito,
)
# Capa Core
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_carritos(db: Session = Depends(get_db)):
    """Obtiene la lista de todos los carritos activos en el sistema."""
    db_carritos = get_carritos(db)
    return success_response(
        data=db_carritos, 
        message="Lista de carritos obtenida"
    )


@router.get("/{carrito_id}")
def obtener_carrito(carrito_id: str, db: Session = Depends(get_db)):
    """Busca un carrito específico por su ID."""
    db_carrito = get_carrito_by_id(db, carrito_id)
    if not db_carrito:
        raise NotFoundError(message=f"El carrito con ID {carrito_id} no existe")
    
    return success_response(data=db_carrito)


@router.post("/")
def crear_nuevo_carrito(carrito: CarritoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo carrito de compras para un usuario."""
    nuevo_carrito = create_carrito(db=db, carrito=carrito)
    return success_response(
        data=nuevo_carrito, 
        message="Carrito creado exitosamente"
    )


@router.put("/{carrito_id}")
def actualizar_carrito(
    carrito_id: str, carrito: CarritoCreate, db: Session = Depends(get_db)
):
    """Actualiza la información de un carrito existente."""
    db_carrito = update_carrito(db, carrito_id, carrito)
    if not db_carrito:
        raise NotFoundError(message="No se pudo actualizar: Carrito no encontrado")
    
    return success_response(
        data=db_carrito, 
        message="Carrito actualizado"
    )


@router.delete("/{carrito_id}")
def eliminar_carrito(carrito_id: str, db: Session = Depends(get_db)):
    """Elimina un carrito del sistema."""
    exito = delete_carrito(db, carrito_id)
    if not exito:
        raise NotFoundError(message="No se pudo eliminar: Carrito no encontrado")
    
    return success_response(
        data=None, 
        message="Carrito eliminado correctamente"
    )