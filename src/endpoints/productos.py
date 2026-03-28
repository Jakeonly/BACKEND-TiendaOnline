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
# Capa Core
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_productos(db: Session = Depends(get_db)):
    """Obtiene todos los productos disponibles en la tienda."""
    db_productos = get_productos(db)
    return success_response(
        data=db_productos, 
        message="Catálogo de productos obtenido"
    )


@router.get("/{producto_id}")
def obtener_producto(producto_id: str, db: Session = Depends(get_db)):
    """Busca un producto por su ID único."""
    db_producto = get_producto_by_id(db, producto_id)
    if not db_producto:
        raise NotFoundError(message=f"El producto con ID {producto_id} no existe")
    
    return success_response(data=db_producto)


@router.post("/")
def crear_nuevo_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Registra un nuevo producto en el inventario."""
    nuevo_prod = create_producto(db=db, producto=producto)
    return success_response(
        data=nuevo_prod, 
        message="Producto creado exitosamente"
    )


@router.put("/{producto_id}")
def actualizar_producto_data(
    producto_id: str, producto: ProductoCreate, db: Session = Depends(get_db)
):
    """Actualiza los detalles de un producto existente."""
    db_producto = update_producto(db, producto_id, producto)
    if not db_producto:
        raise NotFoundError(message="No se pudo actualizar: Producto no encontrado")
    
    return success_response(
        data=db_producto, 
        message="Producto actualizado correctamente"
    )


@router.delete("/{producto_id}")
def eliminar_producto_data(producto_id: str, db: Session = Depends(get_db)):
    """Elimina un producto del sistema."""
    exito = delete_producto(db, producto_id)
    if not exito:
        raise NotFoundError(message="No se pudo eliminar: Producto no encontrado")
    
    return success_response(
        data=None, 
        message="Producto eliminado del inventario"
    )