import uuid
from src.database.config import Base
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Usuario(Base):
    __tablename__ = "tbl_usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre_completo = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True)
    es_admin = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    carritos = relationship("Carrito", back_populates="usuario")
    ordenes = relationship("Orden", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id}, email='{self.email}')>"
