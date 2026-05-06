"""
Script para crear y actualizar el esquema de la BD.
- Crea las tablas definidas en los modelos (create_all).
- Ejecuta migraciones SQL en migrations/ en orden (para alteraciones futuras).

Uso:
  python migrate_db.py

Requiere DATABASE_URL en .env (o entorno). Seguro para ejecutar varias veces.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

import src.entities.usuario
import src.entities.categoria
import src.entities.producto
import src.entities.carrito
import src.entities.detalle_carrito
import src.entities.orden
import src.entities.detalle_orden
import src.entities.descuento
from src.database.config import engine, create_tables

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def ensure_migrations_table(conn):
    """Crea la tabla de control de migraciones si no existe."""
    conn.execute(
        text("""
        CREATE TABLE IF NOT EXISTS _schema_migrations (
            name VARCHAR(255) PRIMARY KEY,
            applied_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
        """)
    )
    conn.commit()


def applied_migrations(conn):
    """Devuelve el set de nombres de migración ya aplicados."""
    r = conn.execute(text("SELECT name FROM _schema_migrations"))
    return {row[0] for row in r}


def run_sql_file(conn, path: Path) -> None:
    """Ejecuta un archivo .sql (sentencias separadas por ;)."""
    sql = path.read_text(encoding="utf-8")

    # Eliminar líneas que son solo comentarios (líneas que empiezan con --)
    lines = [line for line in sql.splitlines() if not line.strip().startswith("--")]
    clean_sql = "\n".join(lines)

    # Separar por ; para obtener sentencias y ejecutar cada una
    statements = [s.strip() for s in clean_sql.split(";") if s.strip()]
    for stmt in statements:
        conn.execute(text(stmt))
    conn.commit()


def run_pending_migrations(conn):
    """Ejecuta los .sql en migrations/ que aún no están aplicados."""
    if not MIGRATIONS_DIR.is_dir():
        return
    applied = applied_migrations(conn)
    files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    for f in files:
        name = f.name
        if name in applied:
            continue
        print(f"  Aplicando migración: {name}")
        run_sql_file(conn, f)
        conn.execute(
            text("INSERT INTO _schema_migrations (name) VALUES (:name)"),
            {"name": name},
        )
        conn.commit()
        applied.add(name)


def main():
    try:
        print("Creando/actualizando tablas desde modelos...")
        create_tables()

        with engine.connect() as conn:
            ensure_migrations_table(conn)
            print("Ejecutando migraciones SQL pendientes...")
            run_pending_migrations(conn)

        print("Migración completada.")
    except OperationalError as e:
        if "password authentication failed" in str(e).lower():
            print("Error: fallo de autenticación con la BD. Revisa DATABASE_URL en .env")
        else:
            print("Error de conexión a la base de datos:", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()