from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.categoria import Categoria
from src.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from src.core.exceptions import NotFoundError
from src.core.responses import success_response

router = APIRouter()


@router.get("/")
def listar_categorias_endpoint(db: Session = Depends(get_db)):
    """Lista todas las categorías de la tienda."""
    db_cats = db.query(Categoria).all()
    data = [
        CategoriaResponse.model_validate(c).model_dump(mode="json") for c in db_cats
    ]
    return success_response(data=data, message="Categorías obtenidas")


@router.get("/{categoria_id}")
def obtener_categoria_endpoint(categoria_id: UUID, db: Session = Depends(get_db)):
    """Obtiene una categoría por su ID."""
    db_cat = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not db_cat:
        raise NotFoundError(message="Categoría no encontrada")
    data = CategoriaResponse.model_validate(db_cat).model_dump(mode="json")
    return success_response(data=data)


@router.post("/", status_code=201)
def crear_categoria_endpoint(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """Crea una nueva categoría."""
    nuevo = Categoria(**categoria.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    data = CategoriaResponse.model_validate(nuevo).model_dump(mode="json")
    return success_response(data=data, message="Categoría creada")


@router.put("/{categoria_id}")
def actualizar_categoria_endpoint(
    categoria_id: UUID, categoria: CategoriaUpdate, db: Session = Depends(get_db)
):
    """Modifica una categoría existente."""
    db_cat = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not db_cat:
        raise NotFoundError(message="Categoría no encontrada")

    for field, value in categoria.model_dump(exclude_unset=True).items():
        setattr(db_cat, field, value)

    db.commit()
    db.refresh(db_cat)

    data = CategoriaResponse.model_validate(db_cat).model_dump(mode="json")
    return success_response(data=data, message="Categoría actualizada")


@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria_endpoint(categoria_id: UUID, db: Session = Depends(get_db)):
    """Borra una categoría."""
    db_cat = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not db_cat:
        raise NotFoundError(message="Categoría no encontrada")

    db.delete(db_cat)
    db.commit()

    return None
