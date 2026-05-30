import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, String, TypeDecorator, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

# Crear TypeDecorator para UUID compatible con SQLite
class GUID(TypeDecorator):
    """Platform-independent GUID type."""
    impl = String(36)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if dialect.name == "postgresql":
            return value
        if not isinstance(value, uuid.UUID):
            return str(uuid.UUID(value)) if value else value
        return str(value)

    def process_result_value(self, value, dialect):
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value) if value else value
        return value


# Monkey-patch antes de importar app y modelos
import src.entities.usuario
import src.entities.producto
import src.entities.categoria
import src.entities.carrito
import src.entities.orden
import src.entities.descuento
import src.entities.detalle_carrito
import src.entities.detalle_orden
import src.entities.pago

# Reemplazar UUID con GUID en las columnas
from sqlalchemy.dialects.postgresql import UUID as OriginalUUID
for module in [src.entities.usuario, src.entities.producto, src.entities.categoria,
               src.entities.carrito, src.entities.orden, src.entities.descuento,
               src.entities.detalle_carrito, src.entities.detalle_orden, src.entities.pago]:
    if hasattr(module, 'OriginalUUID'):
        module.OriginalUUID = GUID

from src.app import app
from src.database.config import Base, get_db

# Crear engine SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override de la dependencia de BD para usar SQLite en memoria."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """Fixture que provee un cliente de pruebas limpio para cada test."""
    # Sobrescribir la dependencia de get_db
    app.dependency_overrides[get_db] = override_get_db
    
    # Crear las tablas
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        # Si falla, ignorar (algunos tests no necesitan tablas)
        pass
    
    client = TestClient(app)
    yield client
    
    # Limpiar después de cada test
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        pass
    app.dependency_overrides.clear()