import uuid
from src.database.config import Base
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Orden(Base):
    __tablename__ = "tbl_ordenes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(15), default="Pendiente")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    usuario_id = Column(
        UUID(as_uuid=True), ForeignKey("tbl_usuarios.id"), nullable=False
    )
    carrito_id = Column(
        UUID(as_uuid=True), ForeignKey("tbl_carritos.id"), nullable=True
    )
    descuento_id = Column(
        UUID(as_uuid=True), ForeignKey("tbl_descuentos.id"), nullable=True
    )

    usuario = relationship("Usuario", back_populates="ordenes")
    descuento = relationship("Descuento", back_populates="ordenes")
    detalles = relationship("DetalleOrden", back_populates="orden")
    pagos = relationship("Pago", back_populates="orden")
    carrito = relationship("Carrito")
