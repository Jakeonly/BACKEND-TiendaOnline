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

DATABASE_URL = os.getenv("DATABASE_URL")


_ssl_mode = os.getenv("SSL_MODE", "require")

engine = (
    create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={"sslmode": _ssl_mode}, 
    )
    if DATABASE_URL
    else None
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    if engine is None:
        raise RuntimeError("DATABASE_URL no configurada.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    if engine is not None:
        Base.metadata.create_all(bind=engine)