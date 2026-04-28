import uuid
from src.database.config import Base
from sqlalchemy import Column, Numeric, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Pago(Base):
    __tablename__ = "tbl_pagos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    monto = Column(Numeric(10, 2), nullable=False)
    metodo = Column(String(50), nullable=False)
    estado = Column(String(20), default="pendiente")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    orden_id = Column(UUID(as_uuid=True), ForeignKey("tbl_ordenes.id"), nullable=False)
    orden = relationship("Orden", back_populates="pagos")
