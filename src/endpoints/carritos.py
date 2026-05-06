from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload  # Importamos joinedload para optimizar
from typing import Any

from src.database.config import get_db
from src.entities.carrito import Carrito
from src.schemas.carrito_schema import CarritoCreate, CarritoUpdate, CarritoResponse
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_carritos_endpoint(db: Session = Depends(get_db)) -> Any:
    """
    Muestra todos los carritos registrados.
    Usamos joinedload para traer la info del usuario y evitar errores de parsing.
    """
    # Cargamos la relación 'usuario' de una vez para que Pydantic no falle[cite: 1]
    db_carritos = db.query(Carrito).options(joinedload(Carrito.usuario)).all()

    # Serialización manual segura para asegurar un JSON limpio
    data = []
    for c in db_carritos:
        data.append({
            "id": str(c.id),
            "usuario_id": str(c.usuario_id),
            "estado": c.estado,
            "usuario_email": c.usuario.email if c.usuario else "Sin asignar",
            "fecha_creacion": c.fecha_creacion.isoformat() if c.fecha_creacion else None,
            "fecha_edicion": c.fecha_edicion.isoformat() if c.fecha_edicion else None,
        })
        
    return success_response(
        data=data, 
        message=f"Se encontraron {len(data)} carritos"
    )

@router.get("/{carrito_id}")
def obtener_carrito_endpoint(carrito_id: UUID, db: Session = Depends(get_db)):
    """Busca un carrito por ID con manejo de error explícito."""
    db_carrito = db.query(Carrito).filter(Carrito.id == carrito_id).first()

    if not db_carrito:
        raise NotFoundError(message=f"El carrito con ID {carrito_id} no existe")

    # Usamos model_validate con from_attributes configurado en el esquema[cite: 1]
    data = CarritoResponse.model_validate(db_carrito).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_carrito_endpoint(carrito: CarritoCreate, db: Session = Depends(get_db)):
    """Crea un carrito asociado a un usuario."""
    nuevo = Carrito(**carrito.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # Devolvemos el objeto creado en formato JSON
    data = CarritoResponse.model_validate(nuevo).model_dump(mode="json")
    return success_response(data=data, message="Carrito creado exitosamente")


@router.put("/{carrito_id}")
def actualizar_carrito_endpoint(
    carrito_id: UUID, carrito: CarritoUpdate, db: Session = Depends(get_db)
):
    """Actualiza la información de un carrito (ej: cambiar el usuario asignado)."""
    db_carrito = db.query(Carrito).filter(Carrito.id == carrito_id).first()

    if not db_carrito:
        raise NotFoundError(message="No se pudo actualizar: Carrito no encontrado")

    # Excluimos campos no enviados para no sobreescribir con Nulos[cite: 1]
    update_data = carrito.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_carrito, field, value)

    db.commit()
    db.refresh(db_carrito)

    data = CarritoResponse.model_validate(db_carrito).model_dump(mode="json")
    return success_response(data=data, message="Carrito actualizado")


@router.delete("/{carrito_id}", status_code=204)
def eliminar_carrito_endpoint(carrito_id: UUID, db: Session = Depends(get_db)):
    """Elimina un carrito y sus dependencias si tiene cascade configurado."""
    db_carrito = db.query(Carrito).filter(Carrito.id == carrito_id).first()

    if not db_carrito:
        raise NotFoundError(message="No se pudo eliminar: Carrito no encontrado")

    db.delete(db_carrito)
    db.commit()
    return None
