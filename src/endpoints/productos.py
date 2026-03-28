from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.producto import Producto
from src.entities.categoria import Categoria
from src.schemas.producto_schema import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: UUID, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("", response_model=ProductoResponse, status_code=201)
def crear_producto(dato: ProductoCreate, db: Session = Depends(get_db)):
    if not db.query(Categoria).filter(Categoria.id == dato.categoria_id).first():
        raise HTTPException(status_code=400, detail="Categoría no encontrada")
    producto = Producto(**dato.model_dump())
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: UUID, dato: ProductoUpdate, db: Session = Depends(get_db)
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    update = dato.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(producto, k, v)
    db.commit()
    db.refresh(producto)
    return producto


@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: UUID, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return None
