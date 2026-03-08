"""
Script para crear las tablas en Neon (PostgreSQL).
Ejecutar una vez después de configurar DATABASE_URL en .env:

  python init_db.py

No es necesario levantar la API; este script solo aplica el esquema.
"""

import os

from dotenv import load_dotenv

# Cargar .env desde la carpeta del proyecto (donde está init_db.py)
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from sqlalchemy.exc import OperationalError

import src.entities.carrito
import src.entities.categoria
import src.entities.descuento
import src.entities.detalle_carrito
import src.entities.detalle_orden
import src.entities.orden
import src.entities.producto
import src.entities.usuario

from src.database.config import create_tables

if __name__ == "__main__":
    try:
        create_tables()
        print("Tablas creadas correctamente en Neon.")
    except OperationalError as e:
        if "password authentication failed" in str(e).lower():
            print("Error: Neon rechazó la contraseña (password authentication failed).")
            print(
                "  - Entra a https://console.neon.tech y revisa la conexión del proyecto."
            )
            print(
                "  - Copia de nuevo la connection string (Connection string) y actualiza .env."
            )
            print(
                "  - Si la contraseña tiene caracteres especiales (& # @ ?), codifícala en URL (ej. @ → %40)."
            )
        else:
            print("Error de conexión a la base de datos:", e)
        raise SystemExit(1)