import uuid
from database.config import Base
from sqlalchemy import Column, String, Numeric, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Descuento(Base):
    __tablename__ = "tbl_descuentos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = Column(String(20), unique=True, nullable=False)
    porcentaje = Column(Numeric(5, 2), nullable=True)
    monto_fijo = Column(Numeric(10, 2), nullable=True)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    ordenes = relationship("Orden", back_populates="descuento")