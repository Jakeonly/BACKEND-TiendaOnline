"""
Seeder: datos iniciales para Tienda Online (dev/QA/prod).
Idempotente: no duplica registros si ya existen (email, nombre o código).

Uso:
  python seed_db.py

Requiere DATABASE_URL y que las tablas ya existan (init_db.py o migrate_db.py).
"""

from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

from src.database.config import SessionLocal
from src.entities.categoria import Categoria
from src.entities.descuento import Descuento
from src.entities.producto import Producto
from src.entities.usuario import Usuario

load_dotenv(Path(__file__).resolve().parent / ".env")


USUARIOS_INICIALES = [
    {
        "nombre_completo": "Administrador Tienda",
        "email": "admin@tienda.local",
        "contraseña": "Admin123!",
        "telefono": "3001234567",
        "direccion": "Cra 10 # 20-30",
        "activo": True,
        "es_admin": True,
    },
    {
        "nombre_completo": "Cliente Demo",
        "email": "cliente@tienda.local",
        "contraseña": "Cliente123!",
        "telefono": "3000000000",
        "direccion": "Calle 45 # 12-55",
        "activo": True,
        "es_admin": False,
    },
]

CATEGORIAS_INICIALES = [
    {
        "nombre": "Tecnología",
        "descripcion": "Dispositivos electrónicos y accesorios.",
    },
    {
        "nombre": "Hogar",
        "descripcion": "Artículos para cocina, limpieza y decoración.",
    },
    {
        "nombre": "Deportes",
        "descripcion": "Implementos y ropa deportiva.",
    },
]

PRODUCTOS_INICIALES = [
    {
        "nombre": "Mouse Inalámbrico",
        "descripcion": "Mouse ergonómico con conexión Bluetooth.",
        "precio": Decimal("79900.00"),
        "stock": 30,
        "categoria": "Tecnología",
    },
    {
        "nombre": "Teclado Mecánico",
        "descripcion": "Teclado mecánico RGB para escritorio.",
        "precio": Decimal("249900.00"),
        "stock": 15,
        "categoria": "Tecnología",
    },
    {
        "nombre": "Sartén Antiadherente",
        "descripcion": "Sartén de 24cm, ideal para uso diario.",
        "precio": Decimal("69900.00"),
        "stock": 20,
        "categoria": "Hogar",
    },
    {
        "nombre": "Mancuernas 5kg",
        "descripcion": "Par de mancuernas recubiertas en neopreno.",
        "precio": Decimal("119900.00"),
        "stock": 12,
        "categoria": "Deportes",
    },
]


def construir_descuentos_iniciales() -> list[dict]:
    ahora = datetime.utcnow()
    return [
        {
            "codigo": "BIENVENIDA10",
            "porcentaje": Decimal("10.00"),
            "monto_fijo": None,
            "fecha_inicio": ahora,
            "fecha_fin": ahora + timedelta(days=180),
        },
        {
            "codigo": "ENVIO5000",
            "porcentaje": None,
            "monto_fijo": Decimal("5000.00"),
            "fecha_inicio": ahora,
            "fecha_fin": ahora + timedelta(days=180),
        },
    ]


def seed_usuarios(db):
    for data in USUARIOS_INICIALES:
        if db.query(Usuario).filter(Usuario.email == data["email"]).first():
            continue
        db.add(Usuario(**data))
        print(f"  Usuario creado: {data['email']}")
    db.commit()


def seed_categorias(db):
    for data in CATEGORIAS_INICIALES:
        if db.query(Categoria).filter(Categoria.nombre == data["nombre"]).first():
            continue
        db.add(Categoria(**data))
        print(f"  Categoría creada: {data['nombre']}")
    db.commit()


def obtener_mapa_categorias(db) -> dict[str, Categoria]:
    categorias = db.query(Categoria).all()
    return {categoria.nombre: categoria for categoria in categorias}


def seed_productos(db):
    mapa_categorias = obtener_mapa_categorias(db)
    for data in PRODUCTOS_INICIALES:
        categoria = mapa_categorias.get(data["categoria"])
        if not categoria:
            continue

        existente = (
            db.query(Producto)
            .filter(
                Producto.nombre == data["nombre"],
                Producto.categoria_id == categoria.id,
            )
            .first()
        )
        if existente:
            continue

        db.add(
            Producto(
                nombre=data["nombre"],
                descripcion=data["descripcion"],
                precio=data["precio"],
                stock=data["stock"],
                categoria_id=categoria.id,
            )
        )
        print(f"  Producto creado: {data['nombre']}")
    db.commit()


def seed_descuentos(db):
    descuentos_iniciales = construir_descuentos_iniciales()
    for data in descuentos_iniciales:
        if db.query(Descuento).filter(Descuento.codigo == data["codigo"]).first():
            continue
        db.add(Descuento(**data))
        print(f"  Descuento creado: {data['codigo']}")
    db.commit()


def main():
    try:
        db = SessionLocal()
        try:
            print("Sembrando usuarios...")
            seed_usuarios(db)
            print("Sembrando categorías...")
            seed_categorias(db)
            print("Sembrando productos...")
            seed_productos(db)
            print("Sembrando descuentos...")
            seed_descuentos(db)
            print("Seed completado.")
        finally:
            db.close()
    except OperationalError as e:
        print("Error de conexión a la base de datos:", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()