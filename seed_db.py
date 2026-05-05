"""
Seeder: datos iniciales para Tienda Online (dev/QA/prod).
Idempotente: no duplica registros si ya existen (email, nombre o código).

Uso:
  python seed_db.py

Requiere DATABASE_URL y que las tablas ya existan (init_db.py o migrate_db.py).
"""

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
import random

from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

from src.database.config import SessionLocal
from src.entities.categoria import Categoria
from src.entities.descuento import Descuento
from src.entities.producto import Producto
from src.entities.usuario import Usuario
from src.entities.carrito import Carrito
from src.entities.detalle_carrito import DetalleCarrito
from src.entities.orden import Orden
from src.entities.detalle_orden import DetalleOrden
from src.entities.pago import Pago

load_dotenv(Path(__file__).resolve().parent / ".env")


USUARIOS_INICIALES = [
    {
        "nombre_completo": "Administrador Tienda",
        "email": "admin@gmail.com",
        "contraseña": "admin123",
        "telefono": "3001234567",
        "direccion": "Cra 10 # 20-30",
        "activo": True,
        "es_admin": True,
    },
    {
        "nombre_completo": "Cliente Demo",
        "email": "cliente@gmail.com",
        "contraseña": "cliente123",
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
    {
        "nombre": "Tarjeta Gráfica RTX 3060",
        "descripcion": "GPU para gaming y productividad.",
        "precio": Decimal("1299900.00"),
        "stock": 8,
        "categoria": "Tecnología",
    },
    {
        "nombre": "Memoria RAM 16GB DDR4",
        "descripcion": "Kit 2x8GB 3200MHz.",
        "precio": Decimal("249900.00"),
        "stock": 40,
        "categoria": "Tecnología",
    },
    {
        "nombre": "Procesador Intel Core i5",
        "descripcion": "CPU 10ma generación para escritorio.",
        "precio": Decimal("749900.00"),
        "stock": 10,
        "categoria": "Tecnología",
    },
    {
        "nombre": "Procesador AMD Ryzen 5",
        "descripcion": "CPU AMD Ryzen para rendimiento balanceado.",
        "precio": Decimal("699900.00"),
        "stock": 12,
        "categoria": "Tecnología",
    },
    {
        "nombre": "SSD 1TB NVMe",
        "descripcion": "Almacenamiento rápido NVMe M.2.",
        "precio": Decimal("399900.00"),
        "stock": 25,
        "categoria": "Tecnología",
    },
]


def construir_descuentos_iniciales() -> list[dict]:
    ahora = datetime.now(timezone.utc)
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
        existente = db.query(Usuario).filter(Usuario.email == data["email"]).first()

        if existente:
            continue

        datos_usuario = data.copy()

        db.add(Usuario(**datos_usuario))
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


def seed_carritos(db):
    cliente = db.query(Usuario).filter(Usuario.email == "cliente@gmail.com").first()
    if not cliente:
        return

    current_count = db.query(Carrito).filter(Carrito.usuario_id == cliente.id).count()
    target = 5
    created = 0
    while current_count < target:
        carrito = Carrito(usuario_id=cliente.id)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
        current_count += 1
        created += 1
        print(f"  Carrito creado para: {cliente.email} (id={carrito.id})")
    if created == 0:
        print(f"  Ya existen {current_count} carritos para {cliente.email}")


def seed_detalle_carrito(db):
    # Poblar todos los carritos del cliente con 1-3 productos preferentemente de Tecnología
    carritos = (
        db.query(Carrito)
        .join(Usuario)
        .filter(Usuario.email == "cliente@gmail.com")
        .all()
    )
    if not carritos:
        return

    productos = db.query(Producto).all()
    if not productos:
        return

    tech_products = [p for p in productos if getattr(p.categoria, "nombre", "") == "Tecnología"]
    pool = tech_products or productos

    for carrito in carritos:
        existing_details = db.query(DetalleCarrito).filter(DetalleCarrito.carrito_id == carrito.id).count()
        if existing_details > 0:
            continue

        picks = random.sample(pool, k=min(len(pool), random.randint(1, 3)))
        for producto in picks:
            cantidad = random.randint(1, 3)
            detalle = DetalleCarrito(
                cantidad=cantidad,
                precio_unitario=producto.precio,
                carrito_id=carrito.id,
                producto_id=producto.id,
            )
            db.add(detalle)
            print(f"  Detalle carrito creado: {producto.nombre} x{cantidad} (carrito={carrito.id})")
        db.commit()


def seed_ordenes(db):
    cliente = db.query(Usuario).filter(Usuario.email == "cliente@gmail.com").first()
    if not cliente:
        return

    carritos = (
        db.query(Carrito)
        .filter(Carrito.usuario_id == cliente.id)
        .all()
    )
    if not carritos:
        return

    descuento = db.query(Descuento).filter(Descuento.codigo == "BIENVENIDA10").first()
    descuento_id = descuento.id if descuento else None

    for carrito in carritos:
        detalles_carrito = db.query(DetalleCarrito).filter(DetalleCarrito.carrito_id == carrito.id).all()
        if not detalles_carrito:
            continue

        total = Decimal("0.00")
        for d in detalles_carrito:
            total += d.cantidad * d.precio_unitario

        aplicado_descuento = False
        if descuento:
            existe_con_desc = db.query(Orden).filter(Orden.descuento_id == descuento_id).first()
            if not existe_con_desc:
                aplicado_descuento = True
                if descuento.porcentaje is not None:
                    total = total * (Decimal("1.00") - descuento.porcentaje / Decimal("100"))
                elif descuento.monto_fijo is not None:
                    total = total - descuento.monto_fijo
                    if total < Decimal("0.00"):
                        total = Decimal("0.00")

        orden_existente = db.query(Orden).filter(Orden.usuario_id == cliente.id, Orden.total == total).first()
        if orden_existente:
            continue

        orden = Orden(total=total, usuario_id=cliente.id, descuento_id=descuento_id if aplicado_descuento else None)
        db.add(orden)
        db.commit()
        db.refresh(orden)
        print(f"  Orden creada: {orden.id} para {cliente.email} - total {orden.total}")

        for d in detalles_carrito:
            subtotal = d.cantidad * d.precio_unitario
            det = DetalleOrden(
                cantidad=d.cantidad,
                precio_unitario=d.precio_unitario,
                subtotal=subtotal,
                orden_id=orden.id,
                producto_id=d.producto_id,
            )
            db.add(det)
        db.commit()
        print(f"  Detalles de orden creados: {len(detalles_carrito)} for order {orden.id}")


def seed_pagos(db):
    ordenes = db.query(Orden).all()
    if not ordenes:
        return

    for orden in ordenes:
        existente = db.query(Pago).filter(Pago.orden_id == orden.id).first()
        if existente:
            continue

        pago = Pago(monto=orden.total, metodo="efectivo", estado="pagada", orden_id=orden.id)
        db.add(pago)
        db.commit()
        print(f"  Pago creado para orden {orden.id} - monto {pago.monto}")


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
            print("Sembrando carritos y detalles de carrito...")
            seed_carritos(db)
            seed_detalle_carrito(db)
            print("Sembrando ordenes, detalles y pagos...")
            seed_ordenes(db)
            seed_pagos(db)
            print("Seed completado.")
        finally:
            db.close()
    except OperationalError as e:
        print("Error de conexión a la base de datos:", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()