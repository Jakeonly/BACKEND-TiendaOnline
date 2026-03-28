import uuid
from src.database.config import Base
from sqlalchemy import Column, String, Text, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Producto(Base):
    __tablename__ = "tbl_productos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    categoria_id = Column(UUID(as_uuid=True), ForeignKey("tbl_categorias.id"), nullable=False)
    
    categoria = relationship("Categoria", back_populates="productos")
    detalles_carrito = relationship("DetalleCarrito", back_populates="producto")
    detalles_orden = relationship("DetalleOrden", back_populates="producto")