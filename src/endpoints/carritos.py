from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.carrito import Carrito
from src.schemas.carrito_schema import CarritoCreate, CarritoUpdate, CarritoResponse
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_carritos_endpoint(db: Session = Depends(get_db)):
    """Muestra todos los carritos registrados."""
    db_carritos = db.query(Carrito).all()
    data = [
        CarritoResponse.model_validate(c).model_dump(mode="json") for c in db_carritos
    ]
    return success_response(data=data)


@router.get("/{carrito_id}")
def obtener_carrito_endpoint(carrito_id: UUID, db: Session = Depends(get_db)):
    """Busca un carrito por ID."""
    db_carrito = db.query(Carrito).filter(Carrito.id == carrito_id).first()
    if not db_carrito:
        raise NotFoundError(message="Carrito no encontrado")
    data = CarritoResponse.model_validate(db_carrito).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_carrito_endpoint(carrito: CarritoCreate, db: Session = Depends(get_db)):
    """Crea un carrito para un usuario."""
    nuevo = Carrito(**carrito.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    data = CarritoResponse.model_validate(nuevo).model_dump(mode="json")
    return success_response(data=data, message="Carrito creado")


@router.put("/{carrito_id}")
def actualizar_carrito_endpoint(
    carrito_id: UUID, carrito: CarritoUpdate, db: Session = Depends(get_db)
):
    """Actualiza la información de un carrito."""
    db_carrito = db.query(Carrito).filter(Carrito.id == carrito_id).first()
    if not db_carrito:
        raise NotFoundError(message="Carrito no encontrado")

    for field, value in carrito.model_dump(exclude_unset=True).items():
        setattr(db_carrito, field, value)

    db.commit()
    db.refresh(db_carrito)

    data = CarritoResponse.model_validate(db_carrito).model_dump(mode="json")
    return success_response(data=data, message="Carrito actualizado")


@router.delete("/{carrito_id}", status_code=204)
def eliminar_carrito_endpoint(carrito_id: UUID, db: Session = Depends(get_db)):
    """Elimina un carrito."""
    db_carrito = db.query(Carrito).filter(Carrito.id == carrito_id).first()
    if not db_carrito:
        raise NotFoundError(message="Carrito no encontrado")

    db.delete(db_carrito)
    db.commit()

    return None
