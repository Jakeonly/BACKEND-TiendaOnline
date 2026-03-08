"""
PROYECTO TIENDA ONLINE - ITM
Menú interactivo completo que gestiona las 8 entidades del sistema.
Ejecuta la API en segundo plano y despliega el menú de consola.
"""

import sys
import threading
import time
import uvicorn 


from dotenv import load_dotenv
load_dotenv() 


sys.path.insert(0, ".")

from src.crud import (
    listar_usuarios, obtener_usuario, crear_usuario, actualizar_usuario, eliminar_usuario,
    listar_productos, obtener_producto, crear_producto, actualizar_producto, eliminar_producto,
    listar_categorias, obtener_categoria, crear_categoria, actualizar_categoria, eliminar_categoria,
    listar_ordenes, obtener_orden, crear_orden, actualizar_orden, eliminar_orden,
    listar_carritos, obtener_carrito, crear_carrito, eliminar_carrito,
    listar_descuentos, obtener_descuento, crear_descuento, actualizar_descuento, eliminar_descuento,
    listar_detalles_carrito, obtener_detalle_carrito, crear_detalle_carrito, actualizar_detalle_carrito, eliminar_detalle_carrito,
    listar_detalles_orden, obtener_detalle_orden, crear_detalle_orden, actualizar_detalle_orden, eliminar_detalle_orden
)

# --- UTILIDAD PARA VISUALIZACIÓN ---

def imprimir_tabla(nombre, lista, campos):
    print(f"\n>>> LISTA DE {nombre.upper()} <<<")
    if not lista:
        print("    (No hay registros actualmente)")
        return
    # Crear encabezado
    header = " | ".join([c.replace("_", " ").upper() for c in campos])
    print(f"    {header}")
    print("    " + "-" * (len(header) + 10))
    # Imprimir filas
    for item in lista:
        fila = " | ".join([str(item.get(c, "N/A")) for c in campos])
        print(f"    {fila}")

# --- MENÚS ESPECÍFICOS POR ENTIDAD ---

def menu_usuarios():
    while True:
        print("\n--- [1] GESTIÓN DE USUARIOS ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0": break
        try:
            if op == "1":
                imprimir_tabla("usuarios", listar_usuarios(), ["id", "nombre_completo", "email", "es_admin"])
            elif op == "2":
                uid = input("ID Usuario: ").strip()
                print(f"  Resultado: {obtener_usuario(uid)}")
            elif op == "3":
                nom = input("Nombre Completo: ").strip()
                em = input("Email: ").strip()
                pwd = input("Contraseña: ").strip()
                adm = input("¿Es admin? (s/n): ").lower() == 's'
                crear_usuario(nombre_completo=nom, email=em, contraseña=pwd, es_admin=adm)
                print("  Usuario creado con éxito.")
            elif op == "4":
                uid = input("ID a actualizar: ").strip()
                nom = input("Nuevo nombre (vacío para omitir): ").strip() or None
                actualizar_usuario(uid, nombre_completo=nom)
                print("  Usuario actualizado.")
            elif op == "5":
                uid = input("ID a eliminar: ").strip()
                eliminar_usuario(uid)
                print("  Usuario eliminado.")
        except Exception as e: print(f"  Error: {e}")

def menu_categorias():
    while True:
        print("\n--- [2] GESTIÓN DE CATEGORÍAS ---")
        print("1. Listar  2. Crear  3. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0": break
        try:
            if op == "1":
                imprimir_tabla("categorías", listar_categorias(), ["id", "nombre", "descripcion"])
            elif op == "2":
                nom = input("Nombre Categoría: ").strip()
                desc = input("Descripción: ").strip()
                crear_categoria(nombre=nom, descripcion=desc)
                print("  Categoría creada.")
            elif op == "3":
                cid = input("ID a eliminar: ").strip()
                eliminar_categoria(cid)
                print("  Categoría eliminada.")
        except Exception as e: print(f"  Error: {e}")

def menu_productos():
    while True:
        print("\n--- [3] GESTIÓN DE PRODUCTOS ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0": break
        try:
            if op == "1":
                imprimir_tabla("productos", listar_productos(), ["id", "nombre", "precio", "stock", "categoria_id"])
            elif op == "2":
                nom = input("Nombre: ").strip()
                pre = float(input("Precio: ") or 0)
                cid = input("ID Categoría: ").strip()
                crear_producto(nombre=nom, precio=pre, categoria_id=cid)
                print("  Producto creado.")
            elif op == "4":
                pid = input("ID a eliminar: ").strip()
                eliminar_producto(pid)
                print("  Producto eliminado.")
        except Exception as e: print(f"  Error: {e}")

def menu_carritos():
    while True:
        print("\n--- [4] GESTIÓN DE CARRITOS Y DETALLES ---")
        print("1. Listar Carritos  2. Crear Carrito  3. Ver Detalles de Carrito  4. Agregar Producto a Carrito  0. Volver")
        op = input("Opción: ").strip()
        if op == "0": break
        try:
            if op == "1":
                imprimir_tabla("carritos", listar_carritos(), ["id", "usuario_id", "fecha_creacion"])
            elif op == "2":
                uid = input("ID Usuario: ").strip()
                crear_carrito(usuario_id=uid)
                print("  Carrito creado.")
            elif op == "3":
                imprimir_tabla("detalles carrito", listar_detalles_carrito(), ["id", "carrito_id", "producto_id", "cantidad", "precio_unitario"])
            elif op == "4":
                cid = input("ID Carrito: ").strip()
                pid = input("ID Producto: ").strip()
                can = int(input("Cantidad: ") or 1)
                pre = float(input("Precio unitario: ") or 0)
                crear_detalle_carrito(cantidad=can, precio_unitario=pre, carrito_id=cid, producto_id=pid)
                print("  Producto agregado al carrito.")
        except Exception as e: print(f"  Error: {e}")

def menu_ordenes():
    while True:
        print("\n--- [5] GESTIÓN DE ÓRDENES Y FACTURACIÓN ---")
        print("1. Listar Órdenes  2. Crear Orden  3. Ver Detalles de Orden  4. Agregar Detalle a Orden  0. Volver")
        op = input("Opción: ").strip()
        if op == "0": break
        try:
            if op == "1":
                imprimir_tabla("órdenes", listar_ordenes(), ["id", "total", "estado", "usuario_id"])
            elif op == "2":
                tot = float(input("Total: ") or 0)
                uid = input("ID Usuario: ").strip()
                est = input("Estado: ").strip() or "pendiente"
                crear_orden(total=tot, usuario_id=uid, estado=est)
                print("  Orden creada.")
            elif op == "3":
                imprimir_tabla("detalles orden", listar_detalles_orden(), ["id", "orden_id", "producto_id", "cantidad", "subtotal"])
            elif op == "4":
                oid = input("ID Orden: ").strip()
                pid = input("ID Producto: ").strip()
                can = int(input("Cantidad: ") or 1)
                pre = float(input("Precio unitario: ") or 0)
                sub = can * pre
                crear_detalle_orden(cantidad=can, precio_unitario=pre, subtotal=sub, orden_id=oid, producto_id=pid)
                print("  Detalle de orden agregado.")
        except Exception as e: print(f"  Error: {e}")

def menu_descuentos():
    while True:
        print("\n--- [6] GESTIÓN DE DESCUENTOS ---")
        print("1. Listar  2. Crear  3. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0": break
        try:
            if op == "1":
                imprimir_tabla("descuentos", listar_descuentos(), ["id", "codigo", "porcentaje", "fecha_fin"])
            elif op == "2":
                cod = input("Código: ").strip()
                por = float(input("Porcentaje: ") or 0)
                ini = input("Fecha Inicio (YYYY-MM-DD): ").strip()
                fin = input("Fecha Fin (YYYY-MM-DD): ").strip()
                crear_descuento(codigo=cod, fecha_inicio=ini, fecha_fin=fin, porcentaje=por)
                print("  Descuento creado.")
            elif op == "3":
                did = input("ID Descuento: ").strip()
                eliminar_descuento(did)
                print("  Descuento eliminado.")
        except Exception as e: print(f"  Error: {e}")

# --- ARRANQUE DEL SISTEMA ---

def _iniciar_api():
    """Ejecuta el servidor FastAPI en un hilo paralelo"""
    # Nota: Asegúrate que tu archivo principal de FastAPI se llame app.py o cambia el nombre aquí
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, log_level="error")

def main():
    print("============================================")
    print("   TIENDA ONLINE API - MENÚ CONSOLA ITM")
    print("============================================")
    
    # Iniciar la API en segundo plano
    server = threading.Thread(target=_iniciar_api, daemon=True)
    server.start()
    
    print("Esperando a que la API inicie...")
    time.sleep(2.5)
    print("API lista en http://localhost:8000\n")

    while True:
        print("\n========== MENÚ PRINCIPAL ==========")
        print("1. Usuarios")
        print("2. Categorías")
        print("3. Productos")
        print("4. Carritos y Detalles")
        print("5. Órdenes y Detalles")
        print("6. Descuentos")
        print("0. Salir del Sistema")
        print("====================================")
        
        opcion = input("Seleccione una categoría: ").strip()
        
        if opcion == "0":
            print("Cerrando aplicación. ¡Hasta luego!")
            break
        elif opcion == "1": menu_usuarios()
        elif opcion == "2": menu_categorias()
        elif opcion == "3": menu_productos()
        elif opcion == "4": menu_carritos()
        elif opcion == "5": menu_ordenes()
        elif opcion == "6": menu_descuentos()
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()