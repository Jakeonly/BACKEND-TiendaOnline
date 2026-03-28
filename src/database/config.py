"""
Configuración de la base de datos PostgreSQL con Neon
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos Neon PostgreSQL
# Obtener la URL completa de conexión desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de SQLAlchemy solo si hay configuración de BD.
# Esto permite importar la app en pipelines que ejecutan smoke tests sin DB.
engine = (
    create_engine(
        DATABASE_URL,
        echo=False,  # Cambiar a True para ver consultas SQL
        pool_pre_ping=True,  # Verificar conexión antes de usar
        pool_recycle=300,  # Reciclar conexiones cada 5 minutos
    )
    if DATABASE_URL
    else None
)

# Crear la sesión; si no hay engine, fallará explícitamente al usar get_db.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos
    """
    if engine is None:
        raise RuntimeError(
            "DATABASE_URL no está configurada. Define la variable para usar endpoints con base de datos."
        )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    if engine is None:
        return
    Base.metadata.create_all(bind=engine)
