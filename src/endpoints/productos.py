from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.producto_schema import ProductoCreate, ProductoResponse
from src.crud.productos import (
    get_productos,
    get_producto_by_id,
    create_producto,
    update_producto,
    delete_producto,
)
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_productos(db: Session = Depends(get_db)):
    """Obtiene todos los productos disponibles."""
    db_productos = get_productos(db)
    data = [
        ProductoResponse.model_validate(p).model_dump(mode="json") for p in db_productos
    ]
    return success_response(data=data, message="Catálogo obtenido")


@router.get("/{producto_id}")
def obtener_producto(producto_id: UUID, db: Session = Depends(get_db)):
    """Busca un producto por su ID."""
    db_prod = get_producto_by_id(db, producto_id)
    if not db_prod:
        raise NotFoundError(message="Producto no encontrado")
    data = ProductoResponse.model_validate(db_prod).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_nuevo_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Registra un nuevo producto en el inventario."""
    nuevo = create_producto(db, producto)
    data = ProductoResponse.model_validate(nuevo).model_dump(mode="json")
    return success_response(data=data, message="Producto creado exitosamente")


@router.put("/{producto_id}")
def actualizar_producto_data(
    producto_id: UUID, producto: ProductoCreate, db: Session = Depends(get_db)
):
    """Actualiza los detalles de un producto."""
    db_prod = update_producto(db, producto_id, producto)
    if not db_prod:
        raise NotFoundError(message="Producto no encontrado")
    data = ProductoResponse.model_validate(db_prod).model_dump(mode="json")
    return success_response(data=data, message="Producto actualizado")


@router.delete("/{producto_id}", status_code=204)
def eliminar_producto_data(producto_id: UUID, db: Session = Depends(get_db)):
    """Elimina un producto del sistema."""
    if not delete_producto(db, producto_id):
        raise NotFoundError(message="Producto no encontrado")
    return None
