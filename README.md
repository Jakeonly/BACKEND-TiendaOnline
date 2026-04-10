# BACKEND-TiendaOnline

## Sistema de información para una tienda online
Este proyecto es un sistema de gestión para una tienda en línea desarrollado como parte del programa de formación en el ITM. El sistema ofrece un backend robusto construido con FastAPI y un menú interactivo por consola para gestionar el ciclo de vida completo de una tienda, desde usuarios y productos hasta órdenes de compra y descuentos.

### 🚀 Características Principales
- **API REST**: Implementada con FastAPI para un alto rendimiento y documentación automática.
- **Gestión de Base de Datos**: Uso de SQLAlchemy como ORM para interactuar con la base de datos y Alembic para la gestión de migraciones.
- **Seguridad**: Codificación de contraseñas mediante bcrypt.
- **Interfaz de Consola**: Un menú interactivo que permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) directamente desde la terminal.
- **Ejecución Híbrida**: El sistema lanza el servidor de la API en un hilo de ejecución paralelo (background) mientras despliega el menú de usuario en el hilo principal.

### 🛠️ Tecnologías Utilizadas
- **FastAPI**: Framework web moderno.
- **Uvicorn**: Servidor ASGI para la ejecución de la API.
- **SQLAlchemy**: Mapeo objeto-relacional (ORM).
- **PostgreSQL (psycopg2)**: Adaptador para la base de datos.
- **Pydantic**: Validación de esquemas y datos (incluye validador de emails).
- **Python-dotenv**: Manejo de variables de entorno para configuración segura.

### 📂 Entidades del Sistema
El sistema gestiona integralmente las siguientes 8 entidades:

- **Usuarios**: Gestión de clientes y administradores.
- **Categorías**: Clasificación de productos.
- **Productos**: Catálogo de artículos, precios y stock.
- **Carritos**: Gestión de carritos de compras por usuario.
- **Detalles de Carrito**: Artículos específicos dentro de un carrito.
- **Órdenes**: Registro de pedidos realizados.
- **Detalles de Orden**: Facturación detallada de cada pedido.
- **Descuentos**: Manejo de códigos promocionales y porcentajes de rebaja.

### 🔧 Instalación y Configuración
1. **Clonar el repositorio**:
   ```bash
   git clone [https://github.com/Jakeonly/BACKEND-TiendaOnline.git]
   cd BACKEND-TiendaOnline
   ```

2. **Instalar dependencias**:
   Se recomienda usar un entorno virtual:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**:
   Crea un archivo `.env` en la raíz del proyecto con la configuración de tu base de datos y otras variables necesarias.

### 💻 Ejecución
Para iniciar tanto el servidor API como el menú de consola, ejecuta el archivo principal:
```bash
python main.py
```
Al iniciar, la API estará disponible en `http://localhost:8000` y podrás interactuar con el sistema a través de las opciones numeradas en tu terminal.

### 📝 Estructura del Proyecto
- `main.py`: Punto de entrada que coordina el hilo de la API y el menú interactivo.
- `src/app.py`: Configuración y arranque de FastAPI.
- `src/crud/`: Lógica de negocio para las operaciones en la base de datos.
- `src/entities/`: Definición de los modelos de la base de datos.
- `src/schemas/`: Esquemas de Pydantic para validación de datos.
- `src/database/`: Configuración de la conexión a la base de datos.

### 🔐 Seguridad implementada (JWT + CORS)

Resumen de lo que se implementó en este proyecto:

- **Login JWT real en la API**: `POST /usuarios/login` valida por `email` + `contraseña`, verifica usuario activo y administrador, y devuelve `access_token` tipo `bearer`.
- **Token usado en el cliente de consola**: en `main.py` se añadió opción de **Iniciar sesión** y **Cerrar sesión**. Tras login exitoso, el token se guarda y se envía automáticamente en peticiones posteriores.
- **Rutas de usuarios protegidas**: listar, obtener, actualizar y eliminar usuario requieren JWT.
- **Contraseñas hasheadas con bcrypt**: se reforzó validación para evitar error 500 cuando existe hash inválido en BD.
- **CORS activo en FastAPI**: configurado en `src/app.py` con orígenes desde `CORS_ORIGINS`, credenciales habilitadas, métodos comunes y cabeceras `Authorization`, `Content-Type`, `Accept`.

Variables de entorno relevantes (archivo `.env`):

- `JWT_SECRET_KEY`
- `JWT_ALGORITHM` (por defecto `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `CORS_ORIGINS`
- `DATABASE_URL`

Además, se agregó `.env.example` para subir al repositorio sin exponer secretos reales.
