from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.producto import Producto
from src.schemas.producto_schema import ProductoCreate, ProductoUpdate, ProductoResponse
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_productos_endpoint(db: Session = Depends(get_db)):
    """Obtiene todos los productos disponibles."""
    db_productos = db.query(Producto).all()
    data = [
        ProductoResponse.model_validate(p).model_dump(mode="json") for p in db_productos
    ]
    return success_response(data=data, message="Catálogo obtenido")


@router.get("/{producto_id}")
def obtener_producto_endpoint(producto_id: UUID, db: Session = Depends(get_db)):
    """Busca un producto por su ID."""
    db_prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_prod:
        raise NotFoundError(message="Producto no encontrado")
    data = ProductoResponse.model_validate(db_prod).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_nuevo_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Registra un nuevo producto en el inventario."""
    nuevo = Producto(**producto.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    data = ProductoResponse.model_validate(nuevo).model_dump(mode="json")
    return success_response(data=data, message="Producto creado exitosamente")


@router.put("/{producto_id}")
def actualizar_producto_data(
    producto_id: UUID, producto: ProductoUpdate, db: Session = Depends(get_db)
):
    """Actualiza los detalles de un producto."""
    db_prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_prod:
        raise NotFoundError(message="Producto no encontrado")

    for field, value in producto.model_dump(exclude_unset=True).items():
        setattr(db_prod, field, value)

    db.commit()
    db.refresh(db_prod)

    data = ProductoResponse.model_validate(db_prod).model_dump(mode="json")
    return success_response(data=data, message="Producto actualizado")


@router.delete("/{producto_id}", status_code=204)
def eliminar_producto_data(producto_id: UUID, db: Session = Depends(get_db)):
    """Elimina un producto del sistema."""
    db_prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_prod:
        raise NotFoundError(message="Producto no encontrado")

    db.delete(db_prod)
    db.commit()

    return None
