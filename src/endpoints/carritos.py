from uuid import UUID
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
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_carritos(db: Session = Depends(get_db)):
    """Muestra todos los carritos registrados."""
    db_carritos = get_carritos(db)
    data = [CarritoResponse.model_validate(c).model_dump(mode="json") for c in db_carritos]
    return success_response(data=data)


@router.get("/{carrito_id}")
def obtener_carrito(carrito_id: UUID, db: Session = Depends(get_db)):
    """Busca un carrito por ID."""
    db_carrito = get_carrito_by_id(db, carrito_id)
    if not db_carrito:
        raise NotFoundError(message="Carrito no encontrado")
    data = CarritoResponse.model_validate(db_carrito).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_carrito_data(carrito: CarritoCreate, db: Session = Depends(get_db)):
    """Crea un carrito para un usuario."""
    nuevo = create_carrito(db, carrito)
    data = CarritoResponse.model_validate(nuevo).model_dump(mode="json")
    return success_response(data=data, message="Carrito creado")


@router.put("/{carrito_id}")
def actualizar_carrito_data(
    carrito_id: UUID, carrito: CarritoCreate, db: Session = Depends(get_db)
):
    """Actualiza la información de un carrito."""
    db_carrito = update_carrito(db, carrito_id, carrito)
    if not db_carrito:
        raise NotFoundError(message="Carrito no encontrado")
    data = CarritoResponse.model_validate(db_carrito).model_dump(mode="json")
    return success_response(data=data, message="Carrito actualizado")


@router.delete("/{carrito_id}", status_code=204)
def eliminar_carrito_data(carrito_id: UUID, db: Session = Depends(get_db)):
    """Elimina un carrito."""
    if not delete_carrito(db, carrito_id):
        raise NotFoundError(message="Carrito no encontrado")
    return None