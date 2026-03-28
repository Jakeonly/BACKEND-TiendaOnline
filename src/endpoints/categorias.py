from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.database.config import get_db
from src.schemas.categoria_schema import CategoriaCreate, CategoriaResponse
from src.crud.categoria import (
    get_categorias,
    get_categoria_by_id,
    create_categoria,
    update_categoria,
    delete_categoria,
)
# Capa Core
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_todas_las_categorias(db: Session = Depends(get_db)):
    """Obtiene el listado de categorías de productos."""
    db_categorias = get_categorias(db)
    return success_response(
        data=db_categorias, 
        message="Categorías obtenidas correctamente"
    )


@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: str, db: Session = Depends(get_db)):
    """Busca una categoría específica por su ID."""
    db_categoria = get_categoria_by_id(db, categoria_id)
    if not db_categoria:
        raise NotFoundError(message=f"La categoría con ID {categoria_id} no existe")
    
    return success_response(data=db_categoria)


@router.post("/")
def crear_nueva_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """Crea una nueva categoría para organizar productos."""
    nueva_cat = create_categoria(db=db, categoria=categoria)
    return success_response(
        data=nueva_cat, 
        message="Categoría creada exitosamente"
    )


@router.put("/{categoria_id}")
def actualizar_categoria_data(
    categoria_id: str, categoria: CategoriaCreate, db: Session = Depends(get_db)
):
    """Actualiza el nombre o descripción de una categoría."""
    db_categoria = update_categoria(db, categoria_id, categoria)
    if not db_categoria:
        raise NotFoundError(message="No se pudo actualizar: Categoría no encontrada")
    
    return success_response(
        data=db_categoria, 
        message="Categoría actualizada"
    )


@router.delete("/{categoria_id}")
def eliminar_categoria_data(categoria_id: str, db: Session = Depends(get_db)):
    """Elimina una categoría del sistema."""
    exito = delete_categoria(db, categoria_id)
    if not exito:
        raise NotFoundError(message="No se pudo eliminar: Categoría no encontrada")
    
    return success_response(
        data=None, 
        message="Categoría eliminada exitosamente"
    )