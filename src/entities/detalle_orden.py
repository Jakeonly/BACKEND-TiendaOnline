import uuid
from database.config import Base
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class DetalleOrden(Base):
    __tablename__ = "tbl_detalle_orden"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), insert_default=0) 
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    orden_id = Column(UUID(as_uuid=True), ForeignKey("tbl_ordenes.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("tbl_productos.id"), nullable=False)

    orden = relationship("Orden", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_orden")