import uuid
from database.config import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Carrito(Base):
    __tablename__ = "tbl_carritos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estado = Column(String(10), default="activo")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    usuario_id = Column(UUID(as_uuid=True), ForeignKey("tbl_usuarios.id"), nullable=False)
    
    usuario = relationship("Usuario", back_populates="carritos")
    detalles = relationship("DetalleCarrito", back_populates="carrito", cascade="all, delete-orphan")