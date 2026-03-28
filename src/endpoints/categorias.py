from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.categoria_schema import CategoriaCreate, CategoriaResponse

from src.crud.categoria import (
    listar_categorias,
    obtener_categoria,
    crear_categoria,
    actualizar_categoria,
    eliminar_categoria,
)
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_categorias_endpoint(db: Session = Depends(get_db)):
    """Lista todas las categorías de la tienda."""
    # Llamamos a listar_categorias del CRUD
    db_cats = listar_categorias(db)
    data = [
        CategoriaResponse.model_validate(c).model_dump(mode="json") for c in db_cats
    ]
    return success_response(data=data, message="Categorías obtenidas")


@router.get("/{categoria_id}")
def obtener_categoria_endpoint(categoria_id: UUID, db: Session = Depends(get_db)):
    """Obtiene una categoría por su ID."""
    db_cat = obtener_categoria(db, categoria_id)
    if not db_cat:
        raise NotFoundError(message="Categoría no encontrada")
    data = CategoriaResponse.model_validate(db_cat).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_categoria_endpoint(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """Crea una nueva categoría."""
    nuevo = crear_categoria(db, categoria)
    data = CategoriaResponse.model_validate(nuevo).model_dump(mode="json")
    return success_response(data=data, message="Categoría creada")


@router.put("/{categoria_id}")
def actualizar_categoria_endpoint(
    categoria_id: UUID, categoria: CategoriaCreate, db: Session = Depends(get_db)
):
    """Modifica una categoría existente."""
    db_cat = actualizar_categoria(db, categoria_id, categoria)
    if not db_cat:
        raise NotFoundError(message="Categoría no encontrada")
    data = CategoriaResponse.model_validate(db_cat).model_dump(mode="json")
    return success_response(data=data, message="Categoría actualizada")


@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria_endpoint(categoria_id: UUID, db: Session = Depends(get_db)):
    """Borra una categoría."""
    if not eliminar_categoria(db, categoria_id):
        raise NotFoundError(message="Categoría no encontrada")
    return None
